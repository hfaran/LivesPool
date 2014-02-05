from tornado_json.utils import io_schema

from cutthroat.handlers import APIHandler


class Login(APIHandler):

    """Handle authentication"""

    apid = {}
    apid["post"] = {
        "input_schema": {
            "required": ["name", "password"],
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        },
        "doc": """
POST the required credentials to get back a cookie

* `name`: Username
* `password`: Password
"""
    }

    @io_schema
    def post(self, body):
        player_name = body["name"]
        password = body["password"]

        if self.db_conn.auth_user(player_name, password):
            self.set_secure_cookie("user", player_name)
            return {"name": player_name}
        else:
            self.fail("Bad username/password combo")
