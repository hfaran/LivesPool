from tornado_json.utils import io_schema, api_assert
from tornado.web import authenticated

from cutthroat.handlers import APIHandler


class CreateRoom(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
                "owner": {"type": "string"},
            },
            "required": ["name", "owner"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        },
        "doc": """
POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if you wish to keep entry restricted to players who know the password
* `owner`: Name of the player creating the room
"""
    }

    @io_schema
    def post(self, body):
        self.db_conn.create_room(
            room_name=body["name"],
            password=body.get("password") if body.get("password") else "",
            owner=body["owner"]
        )
        return {"name": body["name"]}


class JoinRoom(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
                "player": {"type": "string"},
            },
            "required": ["name", "player"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        },
        "doc": """
POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if it has one
* `player`: Name of player joining the room
"""
    }

    @io_schema
    @authenticated
    def post(self, body):
        self.db_conn.join_room(
            room_name=body["name"],
            password=body.get("password") if body.get("password") else "",
            player_name=body["player"]
        )
        return {"name": body["name"]}


class ListRooms(APIHandler):

    """ListRooms"""

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "array",
        },
        "doc": """
GET to receive list of rooms
"""
    }

    @io_schema
    @authenticated
    def get(self, body):
        return self.db_conn.list_rooms()


class LeaveRoom(APIHandler):

    """"""
    #raise NotImplementedError


class RetireRoom(APIHandler):

    """"""
    # If owner of the room wants to delete it
    #raise NotImplementedError
