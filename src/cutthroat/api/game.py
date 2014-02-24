import uuid
from random import shuffle, choice
from tornado.web import authenticated
from tornado_json.utils import io_schema, api_assert, APIError

from cutthroat.handlers import APIHandler
from cutthroat.db2 import Player, Game, stringify_list
from cutthroat.common import (
    get_player, get_room, get_balls_on_table, get_game_winner, get_game
)
from cutthroat.dblock import DBLock


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

    @authenticated
    @io_schema
    def post(self):
        """POST RequestHandler"""
        game_id = uuid.uuid4().hex
        gamemaster = self.get_current_user()
        player = get_player(self.db_conn, gamemaster)
        room_name = player["current_room"]
        room = get_room(self.db_conn, room_name)
        api_assert(room["owner"] == gamemaster, 403,
                   log_message="You must own a room to create a game.")

        player_names = room["current_players"]
        nplayers = len(player_names)
        nbpp = self.body["nbpp"]

        # Make sure values make sense
        api_assert(nplayers <= nbpp * nplayers <= TOTAL_NUM_BALLS, 400,
                   log_message=("Your math seems to be a little off; "
                                "please pick a `number of balls per player` "
                                "such that each player has at least one ball "
                                "and there are enough to go around for "
                                "everyone.")
                   )

        # Create set of 15 balls, shuffle, and then match to players
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

        # Create game
        self.db_conn["games"].insert(
            {
                "game_id": game_id,
                "players": stringify_list(players.keys()),
                "orig_players": stringify_list(players.keys()),
                "unclaimed_balls": stringify_list(unclaimed_balls),
                "orig_unclaimed_balls": stringify_list(unclaimed_balls),
                "gamemaster": gamemaster,
                "winner": None
            }
        )
        # Assign each player their set of balls, set game, leave room
        for name, balls in players.iteritems():
            p = get_player(self.db_conn, name)
            p["current_game_id"] = game_id
            p["balls"] = balls
            p["orig_balls"] = balls
            p["current_room"] = None
        # The room can be deleted
        self.db_conn["rooms"].delete(name=room_name)

        return {"game_id": game_id}


class LeaveGame(APIHandler):
    apid = {}
    apid["delete"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object",
            "properties": {
                "game_id": {"type": "string"}
            },
            "required": ["game_id"]
        },
        "doc": """
DELETE to remove yourself from current game
"""
    }

    @authenticated
    @io_schema
    def delete(self):
        # Get player and the game_id he's in
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        game_id = player["current_game_id"]
        api_assert(game_id, 409,
                   log_message="You are not currently in a game.")

        with DBLock():
            # Get game
            game = Game(self.db_conn, "game_id", game_id)

            # Get remaining set of players
            rem_players = list(set(game["players"]) - {player_name})

            # Set new gamemaster
            if not rem_players:
                game["gamemaster"] = None
            # If gamemaster is leaving, assign to a random player
            elif game["gamemaster"] == player_name:
                game["gamemaster"] = choice(rem_players)

            # Set remaining players in game and add players' balls to game's
            #   unclaimed set
            game["players"] = rem_players
            game["unclaimed_balls"] += player["balls"]

            # Set the player's game_id to None and his list of balls to empty
            player["current_game_id"] = None
            player["balls"] = []

        return {"game_id": game_id}


class ToggleBall(APIHandler):
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
POST the required parameters to register the pocketing/unpocketing of a ball

* `ball`: The ball that was pocketed/unpocketed
"""
    }

    @authenticated
    @io_schema
    def post(self):
        gamemaster = self.get_current_user()
        ball = self.body['ball']
        game_id = get_player(self.db_conn, gamemaster)["current_game_id"]
        game = Game(self.db_conn, "game_id", game_id)

        res = {"game_id": game_id}

        # Authenticate
        api_assert(
            game["gamemaster"] == gamemaster,
            401,
            log_message="You are not the gamemaster of the current game"
        )

        # If ball is already sunk, retable it
        if ball not in get_balls_on_table(self.db_conn, game_id):
            game = Game(self.db_conn, "game_id", game_id)
            # Look for ball in game's set of unclaimed balls
            if ball in game["orig_unclaimed_balls"]:
                game["unclaimed_balls"] += [ball]
            # If it's not there, look for it from each player's set
            else:
                for pname in game["players"]:
                    p = Player(self.db_conn, "name", pname)
                    if ball in p["orig_balls"]:
                        p["balls"] += [ball]
                        break
            res['message'] = "Ball {} was retabled.".format(ball)
            return res

        # Otherwise, sink the ball
        # Look for it in players' first
        for pname in Game(self.db_conn, "game_id", game_id)["players"]:
            p = get_player(self.db_conn, pname)
            if ball in p["balls"]:
                p["balls"] = list(set(p["balls"]) - {ball})
                break
        else:
            # Remove ball from unclaimed
            g = Game(self.db_conn, "game_id", game_id)
            uballs = list(game["unclaimed_balls"])
            uballs.remove(ball)
            game["unclaimed_balls"] = uballs

        res["message"] = "Ball {} was sunk.".format(ball)
        return res


class GameState(APIHandler):

    """State of the current game"""

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object",
            "properties": {
                "balls_on_table": {"type": "array"},
                "winner": {"type": "string"},
            },
        },
        "output_example": {
            "winner": "Guy",
            "balls_on_table": [2, 5, 9, 6],
        },
        "doc": """
GET to receive state of current_game

`winner`: Potential winner of the game, or empty string
`balls_on_table`: Array of balls still on the table
"""
    }

    @authenticated
    @io_schema
    def get(self):
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        game_id = player["current_game_id"]
        api_assert(game_id, 400, log_message="You are not currently in"
                   " a game.")

        res = {}
        res["balls_on_table"] = get_balls_on_table(self.db_conn, game_id)
        res["winner"] = get_game_winner(self.db_conn, game_id)

        return res


class ListPlayers(APIHandler):

    """List players in game"""

    apid = {}
    apid["get"] = {
        "input_schema": None,
        "output_schema": {
            "type": "object",
            "properties": {
                "gamemaster": {"type": "string"},
                "players": {"type": "array"},
            },
            "required": ["gamemaster", "players"],
        },
        "output_example": {
            "gamemaster": "Stark",
            "players": ["Stark", "Stannis", "Baratheon", "Tyrell", "Lannister"]
        },
        "doc": """
GET to receive list of players in current game

* `players` array includes ALL players (including gamemaster)
* `gamemaster` field is useful for highlighting the gamemaster in the UI
"""
    }

    @authenticated
    @io_schema
    def get(self):
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        game_id = player["current_game_id"]
        api_assert(game_id, 400, log_message="You are not currently in"
                   " a game.")

        game = Game(self.db_conn, "game_id", game_id)
        return {
            "players": game["players"],
            "gamemaster": game["gamemaster"]
        }


class EndGame(APIHandler):

    """End the game"""

    apid = {}
    apid["delete"] = {
        "input_schema": None,
        "output_schema": {"type": "string"},
        "output_example": "Game 12345678910 was completed; Guy was the winner.",
        "doc": """
DELETE to end the game; this endpoint should only be triggered if GameState indicates there is a winner.
"""
    }

    @authenticated
    @io_schema
    def delete(self):
        player_name = self.get_current_user()
        player = Player(self.db_conn, "name", player_name)
        game_id = player["current_game_id"]
        api_assert(game_id, 400, log_message="You are not currently in"
                   " a game.")
        game = get_game(self.db_conn, game_id)

        # Authenticate
        api_assert(
            game["gamemaster"] == player_name,
            401,
            log_message="You are not the gamemaster of the current game."
        )

        with DBLock():
            winner = get_game_winner(self.db_conn, game_id)

            # If there is no current winner, return an error
            if not winner:
                raise APIError(
                    409,
                    log_message="The game currently has no winner."
                )
            # Otherwise, clean up everything
            else:
                # Record the win for the player who won
                player["games_won"] += [game_id]
                game["winner"] = player_name
                # Remove all players from game
                for pname in game["players"]:
                    p = get_player(self.db_conn, pname)
                    p["current_game_id"] = None
                    p["balls"] = []
                    p["orig_balls"] = []
                # Clear the game's "current" attributes
                game["players"] = []
                game["gamemaster"] = None

                return "Game {} was completed; {} was the winner.".format(
                    game_id, player_name
                )
