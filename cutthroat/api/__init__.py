from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema


class CreateGame(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "player_names": {"type": "list"},
                "nbpp": {"type": "number"},
                "password": {"type": "string"}
            },
            "required": ["player_names", "nbpp"]
        },
        "output_schema": {
            "type": "string"
        }
    }

    @io_schema
    def post(self, body):
        """POST RequestHandler"""
        pass
