from tornado import template

from cutthroat.handlers import ViewHandler


class SignIn(ViewHandler):

    """SignIn"""

    def get(self):
        self.render("signin.html")
