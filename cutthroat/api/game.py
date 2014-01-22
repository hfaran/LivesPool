import uuid
import json
from random import shuffle
from itertools import chain

from tornado_json.utils import io_schema, api_assert

from cutthroat.handlers import APIHandler


TOTAL_NUM_BALLS = 15


def generate_balls(num):
    """:returns: list of balls from 1 through num"""
    return map(lambda x: x + 1, range(num))


def balls_sunk(cls, game_id):
    return list(
        set(generate_balls(TOTAL_NUM_BALLS)) - set(
            cls.db_conn.get_balls_on_table(game_id))
    )


class CreateGame(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "room_password": {"type": "string"},
                "nbpp": {"type": "number"},
                "password": {"type": "string"},
                "room_name": {"type": "string"}
            },
            "required": ["nbpp", "password", "room_name"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"}
            }
        },
        "doc": """
POST the required parameters to create a new game

* `nbpp`: Number of balls per player
* `password`: Password for the game; only the gamemaster should have access to this as it allows updates to the game
* `room_name`: Room from which this game is being created
* `room_password`: (Required only if room is passworded) Password for the room from which this game is being created
"""
    }
    raise NotImplementedError
    # Need to fix this RequestHandler to
    # * get player_names from room
    # * Authenticate the room credentials and delete the room

    @io_schema
    def post(self, body):
        """POST RequestHandler"""
        game_id = str(uuid.uuid4())
        player_names = body["player_names"]
        nplayers = len(player_names)
        nbpp = body["nbpp"]
        password = body["password"]

        # Make sure values make sense
        api_assert(nbpp * nplayers < TOTAL_NUM_BALLS, 400,
                   log_message=("There are literally not enough balls to "
                                "accomodate the game you are trying to "
                                "create.")
                   )

        balls = generate_balls(TOTAL_NUM_BALLS)
        shuffle(balls)

        players = {}
        for i in xrange(nplayers):
            _balls = []
            for i in xrange(nbpp):
                _balls.append(balls.pop())
            pname = player_names.pop()
            players[pname] = _balls

        unclaimed_balls = balls[:]

        self.db_conn.create_game(game_id, players, unclaimed_balls, password)

        return {"game_id": game_id}


class SinkBall(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"},
                "ball": {"type": "number"},
                "password": {"type": "string"}
            },
            "required": ["ball", "password", "game_id"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"},
                "message": {"type": "string"}
            },
            "required": ["game_id"]
        },
        "doc": """
POST the required parameters to register the pocketing of a ball

* `ball`: The ball that was pocketed
* `game_id`: The full game_id of the game for which to register
* `password`: Password for the game; must be provided in order to update the game
"""
    }

    @io_schema
    def post(self, body):
        password = body['password']
        ball = body['ball']
        game_id = body['game_id']

        res = {"game_id": game_id}

        # Authenticate
        api_assert(self.db_conn.auth_game_update_request(game_id, password),
                   401, log_message="Bad password: {}".format(password))

        # If ball is already sunk, do nothing
        if ball not in self.db_conn.get_balls_on_table(game_id):
            res['message'] = "Ball {} was not on the table.".format(ball)
            return res

        for p in self.db_conn.get_players_for_game(game_id):
            if ball in self.db_conn.get_balls_for_player(p):
                self.db_conn.remove_ball_for_player(p, ball)
                break
        else:
            self.db_conn.remove_ball_from_unclaimed(game_id, ball)

        return res
