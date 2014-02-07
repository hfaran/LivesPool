import uuid
import json
from random import shuffle
from itertools import chain
from tornado.web import authenticated

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
                "nbpp": {"type": "number"},
            },
            "required": ["nbpp"]
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"}
            }
        },
        "doc": """
POST the required parameter to create a new game; only the owner of a room can make this request

* `nbpp`: Number of balls per player
"""
    }
    #raise NotImplementedError
    # Need to fix this RequestHandler to
    # * get player_names from room
    # * Authenticate the room credentials and delete the room

    @io_schema
    @authenticated
    def post(self, body):
        """POST RequestHandler"""
        game_id = str(uuid.uuid4())
        gamemaster = self.get_current_user()
        room_name = self.db_conn.get_owned_room(gamemaster)

        api_assert(room_name, 403,
                   log_message="You must own a room to create a game.")

        player_names = self.db_conn.get_players_in_room(room_name)
        nplayers = len(player_names)
        nbpp = body["nbpp"]

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

        # Create game, then delete the room
        self.db_conn.create_game(game_id, players, unclaimed_balls, gamemaster)
        self.db_conn.delete_room(gamemaster)

        return {"game_id": game_id}


class SinkBall(APIHandler):
    apid = {}
    apid["post"] = {
        "input_schema": {
            "type": "object",
            "properties": {
                "ball": {"type": "number"},
            },
            "required": ["ball"]
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
"""
    }

    @io_schema
    @authenticated
    def post(self, body):
        gamemaster = self.get_current_user()
        ball = body['ball']
        game_id = self.db_conn._get_player(gamemaster)[1]["current_game_id"]

        res = {"game_id": game_id}

        # Authenticate
        api_assert(
            self.db_conn.auth_game_update_request(game_id, gamemaster),
            401,
            log_message="You are not the gamemaster of the current game"
        )

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
