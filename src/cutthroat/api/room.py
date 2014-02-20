from tornado_json.utils import io_schema, api_assert, APIError
from tornado.web import authenticated

from cutthroat.handlers import APIHandler
from cutthroat.db2 import Player, Room, Game, NotFoundError
from cutthroat.common import get_player


def assert_non_tenant(rh, body):
    player = get_player(rh.db_conn.db, rh.get_current_user())
    player_room = player["current_room"]
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
                "roomname": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["roomname"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "roomname": {"type": "string"}
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
    def post(self):
        # player must not already be in a room
        assert_non_tenant(self, self.body)

        self.db_conn.create_room(
            room_name=self.body["roomname"],
            password=self.body.get("password") if self.body.get("password") else "",
            owner=self.get_current_user()
        )
        self.db_conn.join_room(
            room_name=self.body["roomname"],
            password=self.body.get("password") if self.body.get("password") else "",
            player_name=self.get_current_user()
        )
        return {"roomname": self.body["roomname"]}


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
    def post(self):
        # player must not already be in a room
        assert_non_tenant(self, self.body)

        self.db_conn.join_room(
            room_name=self.body["name"],
            password=self.body.get("password") if self.body.get("password") else "",
            player_name=self.get_current_user()
        )
        return {"name": self.body["name"]}


class ListRooms(APIHandler):

    """ListRooms"""

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "array",
        },
        "output_example": [
            {"name": "Curve", "pwd_req": True},
            {"name": "Cue", "pwd_req": False}
        ],
        "doc": """
GET to receive list of rooms
"""
    }

    @io_schema
    @authenticated
    def get(self):
        return self.db_conn.list_rooms()


class ListPlayers(APIHandler):

    """List players in room"""

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "players": {"type": "array"},
            },
            "required": ["owner", "players"],
        },
        "output_example": {
            "owner": "Stark",
            "players": ["Stark", "Stannis", "Baratheon", "Tyrell", "Lannister"]
        },
        "doc": """
GET to receive list of players in current room

* `players` array includes ALL players (including owner)
* `owner` field is useful for highlighting the room owner in the UI
"""
    }

    @io_schema
    @authenticated
    def get(self):
        db = self.db_conn.db

        # Get player
        player_name = self.get_current_user()
        player = Player(db, "name", player_name)
        room_name = player["current_room"]
        api_assert(room_name, 400, log_message="You are not currently in"
                   " a room.")

        # Get room
        room = Room(db, "name", room_name)
        return {
            "players": room["current_players"],
            "owner": room["owner"]
        }


class LeaveRoom(APIHandler):

    """LeaveRoom"""

    apid = {}
    apid["delete"] = {
        "input_schema": None,
        "output_schema": {
            "type": "string",
        },
        "doc": """
DELETE to leave current room. If the room owner leaves, the room will be deleted.
"""
    }

    @io_schema
    @authenticated
    def delete(self):
        db = self.db_conn.db

        player_name = self.get_current_user()
        player = Player(db, "name", player_name)
        room_name = player["current_room"]
        if room_name:
            room = Room(db, "name", room_name)
        else:
            raise APIError(409, log_message="You are currently not in a room.")

        if room["owner"] == player_name:
            # Set all players' current_room to None
            for pname in room["current_players"]:
                p = Player(db, "name", pname)
                p["current_room"] = None
            # Delete the room
            db["rooms"].delete(name=room_name)
            return "{} successfully deleted {}".format(player_name, room_name)
        else:
            # Set player's current_room to None and remove from room's current_players list
            player["current_room"] = None
            room["current_players"] = [p for p in room["current_players"] if p != player_name]
            return "{} successfully left {}".format(player_name, room_name)
