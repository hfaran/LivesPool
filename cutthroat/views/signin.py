from tornado import template
from tornado.web import authenticated

from cutthroat.handlers import ViewHandler


class SignIn(ViewHandler):

    """SignIn"""

    def get(self):
        self.render("signin.html")


class Landing(ViewHandler):

    """Landing"""

    @authenticated
    def get(self):
        _, player = self.db_conn._get_player(self.get_current_user())
        if player["current_game_id"]:
            raise NotImplementedError
            # self.redirect("<Insert URL to game view here>")
        else:
            self.redirect("/views/room/join")
