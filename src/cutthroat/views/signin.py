from tornado import template
from tornado.web import authenticated

from cutthroat.handlers import ViewHandler
from cutthroat.common import get_player


class SignIn(ViewHandler):

    """SignIn"""

    def get(self):
        self.render("signin.html")


class Landing(ViewHandler):

    """Landing"""

    @authenticated
    def get(self):
        player = get_player(self.db_conn, self.get_current_user())
        if player["current_game_id"]:
            self.redirect("/room/game")
        elif player["current_room"]:
            self.redirect("/room/lobby")
        else:
            self.redirect("/room/join")
