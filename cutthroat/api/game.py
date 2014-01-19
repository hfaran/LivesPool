import uuid
import json
from random import shuffle
from itertools import chain

from tornado_json.requesthandlers import APIHandler
from tornado_json.utils import io_schema, api_assert


TOTAL_NUM_BALLS = 15


def generate_balls(num):
    """:returns: list of balls from 1 through num"""
    return map(lambda x: x + 1, range(num))


class CreateGame(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "player_names": {"type": "array"},
                "nbpp": {"type": "number"},
                "password": {"type": "string"}
            },
            "required": ["player_names", "nbpp"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"}
            }
        },
        "doc": ""
    }

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

        self.db_conn.create_game(game_id, players, unclaimed_balls)

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
                "game_id": {"type": "string"}
            }
        },
        "doc": ""
    }
