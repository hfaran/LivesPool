from tornado_json.utils import io_schema, api_assert
from tornado.web import authenticated

from cutthroat.handlers import APIHandler


def assert_non_tenant(rh, body):
    player_room = rh.db_conn.get_player_room(rh.get_current_user())
    api_assert(
        not player_room,
        409,
        log_message=(
            "{} is already in a room: `{}`. Leave current room"
            " to join a new one.".format(
                rh.get_current_user(),
                player_room
            )
        )
    )


class CreateRoom(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
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
POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if you wish to keep entry restricted to players who know the password
"""
    }

    @io_schema
    @authenticated
    def post(self, body):
        # player must not already be in a room
        assert_non_tenant(self, body)

        self.db_conn.create_room(
            room_name=body["name"],
            password=body.get("password") if body.get("password") else "",
            owner=self.get_current_user()
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
POST the required parameters to create a new room

* `name`: Name of the room
* `password`: (Optional) Password to the room if it has one
"""
    }

    @io_schema
    @authenticated
    def post(self, body):
        # player must not already be in a room
        assert_non_tenant(self, body)

        self.db_conn.join_room(
            room_name=body["name"],
            password=body.get("password") if body.get("password") else "",
            player_name=self.get_current_user()
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
    # raise NotImplementedError


class RetireRoom(APIHandler):

    """"""
    # If owner of the room wants to delete it
    # raise NotImplementedError
