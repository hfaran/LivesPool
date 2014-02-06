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

    @io_schema
    def post(self, body):
        self.db_conn.create_player(body["name"], body["password"])
        return {"name": body["name"]}

    # @io_schema
    # @authenticated
    # def get(self, body):
