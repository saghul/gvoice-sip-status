#!/usr/bin/env python

import os

from google.appengine.dist import use_library
use_library('django', '1.2')

from google.appengine.ext import db, webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from model import ServerState


class RootHandler(webapp.RequestHandler):
    def get(self):
        try:
            obj = ServerState.get_by_key_name('server_state')
        except db.BadKeyError:
            obj = None
        data = {'server_state': obj}
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, data))


def main():
    application = webapp.WSGIApplication([('/', RootHandler)], debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

