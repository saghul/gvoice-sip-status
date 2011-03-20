
from google.appengine.ext import db


class ServerState(db.Model):
    code = db.IntegerProperty()
    reason = db.StringProperty()
    timestamp = db.StringProperty()

