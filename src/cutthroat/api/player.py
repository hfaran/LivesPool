import bcrypt

from tornado.options import options
from tornado.web import authenticated
from tornado_json.exceptions import api_assert
from tornado_json import schema

from cutthroat.handlers import APIHandler
from cutthroat.common import get_player
from cutthroat.dblock import DBLock


class Player(APIHandler):

    @schema.validate(
        input_schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        },
    )
    def post(self):
        """
        POST the required parameters to permanently register a new player

        * `username`: Username of the player
        * `password`: Password for future logins
        """
        player_name = self.body["username"]
        password = self.body["password"]

        with DBLock():
            # Check if a player with the given name already exists
            player_exists = self.db_conn['players'].find_one(name=player_name)
            api_assert(not player_exists, 409,
                       log_message="{} is already registered.".format(player_name))
            # Create a new user/write to DB
            salt = bcrypt.gensalt(rounds=12)
            self.db_conn['players'].insert(
                {
                    "name": player_name,
                    "current_game_id": "",
                    "current_room": "",
                    "balls": "",
                    "salt": salt,
                    "password": bcrypt.hashpw(str(password), salt),
                    "games_won": ""
                }
            )
        # We also do the step of logging the player in after registration
        self.set_secure_cookie(
            "user",
            player_name,
            options.session_timeout_days
        )

        return {"username": player_name}

    @authenticated
    @schema.validate(
        output_schema={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "current_game_id": {"type": "string"},
                "current_room": {"type": "string"},
                "balls": {"type": "array"},
                "orig_balls": {"type": "array"},
            }
        },
    )
    def get(self):
        """
        GET to retrieve player info
        """
        player_name = self.get_current_user()
        player = get_player(self.db_conn, player_name)

        res = dict(player)
        res.pop("password")  # Redact password
        res.pop("salt")  # Redact salt
        res.pop("id")  # Players don't care about this
        # Make the following strings b/c the schema expects strings
        for k in ["current_game_id", "current_room"]:
            if not res[k]:
                res[k] = ""
        return res
