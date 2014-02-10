from tornado_json.utils import io_schema, api_assert

from cutthroat.handlers import APIHandler


class Login(APIHandler):

    """Handle authentication"""

    apid = {}
    apid["post"] = {
        "input_schema": {
            "required": ["username", "password"],
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        },
        "doc": """
POST the required credentials to get back a cookie

* `username`: Username
* `password`: Password
"""
    }

    @io_schema
    def post(self, body):
        player_name = body["username"]
        password = body["password"]

        if self.db_conn.auth_user(player_name, password):
            self.set_secure_cookie("user", player_name)
            return {"username": player_name}
        else:
            api_assert(
                False,
                400,
                log_message="Bad username/password combo"
            )

    def get(self):
        api_assert(
            False,
            403,
            log_message="Please post to {} to get a cookie".format(
                self.get_login_url())
        )
