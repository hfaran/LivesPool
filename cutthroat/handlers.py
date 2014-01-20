from tornado_json import requesthandlers


class AuthMixin(object):

    def get_current_user(self):
        return self.get_secure_cookie("user")


class APIHandler(requesthandlers.APIHandler, AuthMixin):

    """New APIHandler with AuthMixin"""


class ViewHandler(requesthandlers.ViewHandler, AuthMixin):

    """New ViewHandler with AuthMixin"""
