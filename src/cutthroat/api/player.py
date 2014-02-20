import bcrypt
import logging

from tornado.options import options
from tornado.web import authenticated
from tornado_json.utils import io_schema, api_assert, APIError

from cutthroat.handlers import APIHandler
from cutthroat.db2 import NotFoundError
from cutthroat.db2 import Player as db2_Player


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
    def post(self):
        player_name = self.body["username"]
        password = self.body["password"]
        # Create player
        player_exists = self.db_conn.db['players'].find_one(name=player_name)
        api_assert(not player_exists, 409,
                   log_message="{} is already registered.".format(player_name))
        salt = bcrypt.gensalt(rounds=12)
        self.db_conn.db['players'].insert(
            {
                "name": player_name,
                "current_game_id": "",
                "current_room": "",
                "balls": "",
                "salt": salt,
                "password": bcrypt.hashpw(str(password), salt)
            }
        )

        self.set_secure_cookie(
            "user",
            player_name,
            options.session_timeout_days
        )

        return {"username": player_name}

    @io_schema
    @authenticated
    def get(self):
        player_name = self.get_current_user()

        try:
            player = db2_Player(self.db_conn.db, "name", player_name)
        except NotFoundError:
            raise APIError(
                409,
                log_message="No user {} exists.".format(player_name)
            )

        res = dict(player)
        res.pop("password")  # Redact password
        res.pop("salt")  # Redact salt
        res.pop("id")  # Players don't care about this
        return res
