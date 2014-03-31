from tornado_json.exceptions import api_assert, APIError
from tornado_json import schema
from tornado.web import authenticated

from cutthroat.handlers import APIHandler
from cutthroat.db2 import Player, Room
from cutthroat.common import get_player, get_room
from cutthroat.dblock import DBLock


def assert_non_tenant(db, player_name):
    """Assert that player ``player_name`` is not already in a room

    :type  player_name: str
    :raises APIError: If ``player_name`` is already in a room.
    """
    player = get_player(db, player_name)
    player_room = player["current_room"]
    api_assert(
        not player_room,
        409,
        log_message=(
            "{} is already in a room: `{}`. Leave current room"
            " to join a new one.".format(
                player_name,
                player_room
            )
        )
    )


def create_room(db, room_name, password, owner):
    """Create a new room ``room_name``

    Adds entry for room ``room_name`` to the database.
    :raises APIError: If a room with `room_name` has already
        been created.
    """
    api_assert(not db["rooms"].find_one(name=room_name), 409,
               log_message="Room with name `{}` already exists.".format(
                   room_name))

    db["rooms"].insert(
        {
            "name": room_name,
            "password": password,
            "owner": owner,
            "current_players": ""
        }
    )


def join_room(db, room_name, password, player_name):
    """Join room ``room_name``

    Updates ``current_players`` entry for room ``room_name`` with
    player ``player_name`` to the database.

    :raises APIError: If a room with ``room_name`` does not exist;
        or if the password is incorrect for room ``room_name``, or if player
        ``player_name`` does not exist
    """
    # Ensure that the following preconditions are met:
    #   * Correct password to room is give if required
    #   * The player is not already in a room
    room = get_room(db, room_name)
    api_assert(password == room['password'], 403,
               log_message="Bad password for room `{}`.".format(room_name))
    player = get_player(db, player_name)
    api_assert(
        player_name not in room["current_players"],
        409,
        log_message="Player `{}` already in room `{}`".format(
            player_name, room_name)
    )
    # If they are met, add the player to the room
    room["current_players"] += [player_name]
    player["current_room"] = room_name


class CreateRoom(APIHandler):

    @authenticated
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "roomname": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["roomname"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "roomname": {"type": "string"}
            }
        },
    )
    def post(self):
        """
        POST the required parameters to create a new room

        * `name`: Name of the room
        * `password`: (Optional) Password to the room if you wish to keep
            entry restricted to players who know the password
        """
        # Player must not already be in a room
        assert_non_tenant(self.db_conn, self.get_current_user())
        # We create a room, and then add the player to the room
        #   as the owner.
        create_room(
            self.db_conn,
            room_name=self.body["roomname"],
            password=self.body.get("password") if self.body.get(
                "password") else "",
            owner=self.get_current_user()
        )
        join_room(
            db=self.db_conn,
            room_name=self.body["roomname"],
            password=self.body.get("password") if self.body.get(
                "password") else "",
            player_name=self.get_current_user()
        )
        return {"roomname": self.body["roomname"]}


class JoinRoom(APIHandler):

    @authenticated
    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["name"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            }
        },
    )
    def post(self):
        """
        POST the required parameters to create a new room

        * `name`: Name of the room
        * `password`: (Optional) Password to the room if it has one
        """
        # Player must not already be in a room
        assert_non_tenant(self.db_conn, self.get_current_user())
        # Add player to the room
        join_room(
            db=self.db_conn,
            room_name=self.body["name"],
            password=self.body.get("password") if self.body.get(
                "password") else "",
            player_name=self.get_current_user()
        )
        return {"name": self.body["name"]}


class ListRooms(APIHandler):

    """ListRooms"""

    @authenticated
    @schema.validate(
        output_schema={
            "type": "array",
        },
        output_example=[
            {"name": "Curve", "pwd_req": True},
            {"name": "Cue", "pwd_req": False}
        ],
    )
    def get(self):
        """GET to receive list of rooms"""
        return [
            {
                "name": r["name"],
                "pwd_req": bool(r["password"])
            } for r in self.db_conn['rooms'].all()
        ]


class ListPlayers(APIHandler):

    """List players in room"""

    @authenticated
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "owner": {"type": "string"},
                "players": {"type": "array"},
            },
            "required": ["owner", "players"],
        },
        output_example={
            "owner": "Stark",
            "players": ["Stark", "Stannis", "Baratheon", "Tyrell", "Lannister"]
        },
    )
    def get(self):
        """
        GET to receive list of players in current room

        * `players` array includes ALL players (including owner)
        * `owner` field is useful for highlighting the room owner in the UI
        """
        player_name = self.get_current_user()
        # The reason we don't use get_player in a case like
        #   this, is because this is an authenticated method,
        #   so a player with the name of the current user
        #   SHOULD exist; if he doesn't, then that indicates
        #   a problem on our side (if that happens, the user
        #   will see a 500 Internal Server Error) which
        #   is arguably appropriate in this case.
        player = Player(self.db_conn, "name", player_name)
        room_name = player["current_room"]
        api_assert(room_name, 400, log_message="You are not currently in"
                   " a room.")

        # Again, same thing here; if the player has joined
        #   a room, the room name must exist, otherwise, it
        #   indicates a failure somewhere earlier down the line.
        room = Room(self.db_conn, "name", room_name)
        return {
            "players": room["current_players"],
            "owner": room["owner"]
        }


class LeaveRoom(APIHandler):

    """LeaveRoom"""

    @authenticated
    @schema.validate(
        output_schema={"type": "string"},
    )
    def delete(self):
        """
        DELETE to leave current room. If the room owner leaves, the room will be deleted.
        """
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        room_name = player["current_room"]
        if room_name:
            room = Room(self.db_conn, "name", room_name)
        else:
            raise APIError(409, log_message="You are currently not in a room.")

        with DBLock():
            if room["owner"] == player_name:
                # Set all players' current_room to None
                for pname in room["current_players"]:
                    p = Player(self.db_conn, "name", pname)
                    p["current_room"] = None
                # Delete the room
                self.db_conn["rooms"].delete(name=room_name)
                return "{} successfully deleted {}".format(player_name, room_name)
            else:
                # Set player's current_room to None and remove from room's
                #   current_players list
                player["current_room"] = None
                room["current_players"] = [
                    p for p in room["current_players"] if p != player_name]
                return "{} successfully left {}".format(player_name, room_name)
