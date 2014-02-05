from tornado_json import requesthandlers


class APIHandler(requesthandlers.APIHandler):

    """APIHandler"""

    def get_current_user(self):
        return self.get_secure_cookie("user")


class ViewHandler(requesthandlers.ViewHandler):

    """ViewHandler"""

    def get_current_user(self):
        return self.get_cookie("user")
