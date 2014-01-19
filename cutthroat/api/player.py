from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema, api_assert


class CreatePlayer(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"]
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
"""
    }

    @io_schema
    def post(self, body):
        self.db_conn.create_player(body["name"])
        return {"name": body["name"]}
