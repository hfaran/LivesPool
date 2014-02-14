from tornado.web import authenticated
from tornado_json.utils import io_schema, api_assert

from cutthroat.handlers import APIHandler


class Player(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        },
        "doc": """
POST the required parameters to permanently register a new player

* `username`: Username of the player
* `password`: Password for future logins
"""
    }
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object"
        },
        "doc": """
GET to retrieve player info
"""
    }

    @io_schema
    def post(self, body):
        self.db_conn.create_player(body["username"], body["password"])
        self.set_secure_cookie("user", body["username"])

        return {"username": body["username"]}

    @io_schema
    @authenticated
    def get(self, body):
        player_name = self.get_current_user()
        return self.db_conn.player_info(player_name)
