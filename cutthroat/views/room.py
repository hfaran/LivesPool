from tornado import template

from cutthroat.handlers import ViewHandler
from cutthroat import templates as ct_templates


class Join(ViewHandler):

    """Join"""

    def get(self):
        loader = template.Loader("templates")
        self.render("_base.html",
            global_meta_tags=ct_templates.global_meta_tags(),
            title="Sign In",
            bootstrap=ct_templates.load_bootstrap(),
            navbar="",
            banner_title=ct_templates.banner_title("Join a Room"),
            body=loader.load("joinaroom.html").generate(rooms="")
        )
