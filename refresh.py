#!/usr/bin/env python

import logging
import simplejson

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from model import ServerState


class RefreshHandler(webapp.RequestHandler):
    def get(self):
        logging.info('Got refresh request')
        # We try 3 times in a row because if the request is stopped after 10 seconds we wouldn't
        # get any answer. The SIPwPing server will save the value in the cache anyway, so the second (or third)
        # time we try we'll get an answer immediately
        for x in xrange(0, 3):
            try:
                result = urlfetch.fetch(url='http://localhost:8889/options',
                                    method='POST', 
                                    payload=simplejson.dumps({'target_uri':'test@sip.voice.google.com'}),
                                    headers={'Content-Type':'application/json'},
                                    allow_truncated=False,
                                    deadline=10)
                try:
                    d = simplejson.loads(result.content)
                except Exception, e:
                    logging.warning('Error decoding response: %s' % e)
                else:
                    logging.info('Data: %r' % d)
                    obj = ServerState.get_or_insert('server_state')
                    obj.code = int(d.get('code'))
                    obj.reason = d.get('reason')
                    obj.timestamp = d.get('timestamp')
                    obj.put()
                    break
            except urlfetch.Error, e:
                logging.warning('Refresh failed: %s' % e)
        else:
            logging.warning('Could not fetch server state after 3 retries')
        self.response.out.write('')


def main():
    application = webapp.WSGIApplication([('/refresh', RefreshHandler)], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

