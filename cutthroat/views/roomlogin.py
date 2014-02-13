from tornado import template
from tornado.web import authenticated

from cutthroat.handlers import ViewHandler


class RoomLogin(ViewHandler):

    """RoomLogin"""

    @authenticated
    def get(self):
        self.render("roomlogin.html")
