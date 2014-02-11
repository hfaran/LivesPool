from tornado import template

from cutthroat.handlers import ViewHandler


class Join(ViewHandler):

    """Join"""

    def get(self):
        self.render("joinaroom.html")

class Create(ViewHandler):

    """Create"""

    def get(self):
        self.render("createaroom.html")
