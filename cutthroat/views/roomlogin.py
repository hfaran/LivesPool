from tornado import template

from cutthroat.handlers import ViewHandler


class RoomLogin(ViewHandler):

    """RoomLogin"""

    def get(self):
        self.render("roomlogin.html")