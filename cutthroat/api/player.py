from tornado.web import authenticated
from tornado_json.utils import io_schema, api_assert

from cutthroat.handlers import APIHandler


class Player(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["name", "password"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        },
        "doc": """
POST the required parameters to permanently register a new player

* `name`: Username of the player
* `password`: Password for future logins
"""
    }
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object"
        },
        "doc": """
GET with following query parameters to retrieve player info

* `username`: Username of the player
"""
    }

    @io_schema
    def post(self, body):
        self.db_conn.create_player(body["name"], body["password"])
        return {"name": body["name"]}

    @io_schema
    @authenticated
    def get(self, body):
        player_name = self.get_argument("username")
        if player_name == self.get_current_user():
            return self.db_conn.player_info(player_name)
        else:
            api_assert(
                False,
                403,
                "Please authenticate as `{0}` to view `{0}`'s info.".format(
                    player_name
                )
            )
