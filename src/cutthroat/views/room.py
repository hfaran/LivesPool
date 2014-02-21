from tornado import template
from tornado.web import authenticated

from cutthroat.handlers import ViewHandler
from cutthroat.db2 import Player


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
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        self.render("roomlobby.html", room_name=player["current_room"])


class Game(ViewHandler):

    """Game"""

    @authenticated
    def get(self):
        self.render("game.html")
