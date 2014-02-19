from tornado import template
from tornado.web import authenticated

from cutthroat.handlers import ViewHandler


class Join(ViewHandler):

    """Join"""

    @authenticated
    def get(self):
        self.render("joinaroom.html")


class Create(ViewHandler):

    """Create"""

    @authenticated
    def get(self):
        self.render("createaroom.html")

class Lobby(ViewHandler):

    """Lobby"""

    @authenticated
    def get(self):
        self.render("roomlobby.html")

class Game(ViewHandler):

    """Game"""

    @authenticated
    def get(self):
        self.render("game.html")

