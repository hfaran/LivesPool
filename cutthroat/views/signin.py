from uuid import uuid4
from tornado import template

from cutthroat.handlers import ViewHandler
from cutthroat import templates as ct_templates


class SignIn(ViewHandler):

    """SignIn"""

    def get(self):
        loader = template.Loader("templates")
        self.render("_base.html",
            global_meta_tags=ct_templates.global_meta_tags(),
            title="Sign In",
            bootstrap=ct_templates.load_bootstrap(),
            navbar="",
            banner_title=ct_templates.banner_title("Lives Pool"),
            body=loader.load("signin.html").generate()
        )
