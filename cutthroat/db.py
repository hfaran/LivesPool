import bcrypt
import logging
import dataset
from itertools import chain
from random import choice

from tornado.options import options
from tornado_json.utils import api_assert


def stringify_list(l):
    """Stringify list `l`

    :returns: A comma-joined string rep of `l`
    :rtype: str
    """
    return ",".join(map(str, l))


def listify_string(func, s):
    """'Decode' `s` into a list

    :returns: A list of elements from a comma-split of s each wrapped
        with func
    :rtype: list
    """
    if not s:
        return []
    else:
        return map(func, s.split(","))


class Connection(object):

    """Connection to cutthroat MySQL database"""

    def __init__(self):
        self.db = dataset.connect('sqlite:///{}'.format(options.sqlite_db))

    def create_game(self, game_id, players, unclaimed_balls, gamemaster):
        """Create game with game_id `game_id`

        Adds entry for a new game with given parameters to database, and
        updates players as well.
        :raises APIError: If any players are not already registered
        """
        ptable = self.db['players']
        all_players = [p['name'] for p in ptable]
        api_assert(all(p in all_players for p in players), 409,
                   log_message="Your list of players contains unregistered"
                   " names. Please register all players first.")

        table = self.db['games']
        table.insert(
            {
                "game_id": game_id,
                "players": stringify_list(players.keys()),
                "unclaimed_balls": stringify_list(unclaimed_balls),
                "gamemaster": gamemaster,
                "status": "active"
            }
        )

        table = self.db['players']
        for name, balls in players.iteritems():
            table.update(
                {
                    "name": name,
                    "current_game_id": game_id,
                    "balls": stringify_list(balls),
                },
                ['name']
            )

    def create_player(self, player_name, password):
        """Register new player `player_name`

        Adds entry for player `player_name` to the database.
        :raises APIError: If a player with `player_name` is already
            registered.
        """
        ptable = self.db['players']
        all_players = [p['name'] for p in ptable]
        api_assert(player_name not in all_players, 409,
                   log_message="{} is already registered.".format(player_name))

        salt = bcrypt.gensalt(rounds=12)

        ptable.insert(
            {
                "name": player_name,
                "current_game_id": "",
                "current_room": "",
                "balls": "",
                "salt": salt,
                "password": bcrypt.hashpw(str(password), salt)
            }
        )

    def get_balls_for_player(self, player_name):
        """
        :returns: Balls belonging to player `player_name`
        :rtype: [int, ...]
        """
        table = self.db['players']
        return listify_string(int, table.find_one(name=player_name)['balls'])

    def remove_ball_for_player(self, player_name, ball):
        """Remove `ball` from `player_name`'s active list of balls"""
        balls = self.get_balls_for_player(player_name)
        balls.remove(ball)

        table = self.db['players']
        table.update(dict(name=player_name, balls=stringify_list(balls)),
                     ['name'])

    def remove_ball_from_unclaimed(self, game_id, ball):
        """Remove `ball` from `game_id`'s list of unclaimed_balls"""
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        unclaimed_balls = listify_string(int, game['unclaimed_balls'])
        unclaimed_balls.remove(ball)
        table.update(dict(game_id=game_id, unclaimed_balls=stringify_list(
            unclaimed_balls)),
            ['game_id']
        )

    def get_players_for_game(self, game_id):
        """
        :returns: Players participating in game `game_id`
        :rtype: [str, ...]
        """
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        players = listify_string(str, game['players'])
        return players

    def get_balls_on_table(self, game_id):
        """
        :returns: Balls currently on the table for game `game_id`
        :rtype: [int, ...]
        """
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        players = listify_string(str, game['players'])
        unclaimed_balls = listify_string(int, game['unclaimed_balls'])

        return list(
            chain(*[self.get_balls_for_player(p) for p in players])
        ) + unclaimed_balls

    def auth_game_update_request(self, game_id, gamemaster):
        """
        :returns: Boolean indicating whether `gamemaster` matches the gamemaster-
            entry in the database for `game_id`
        :rtype: bool
        """
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        return game['gamemaster'] == gamemaster

    def auth_user(self, player_name, password):
        ptable = self.db['players']
        player = ptable.find_one(name=player_name)
        api_assert(player, 409,
                   log_message="No user {} exists.".format(player_name))
        return bcrypt.hashpw(
            str(password), str(player["salt"])
        ) == player['password']

    def mark_stale_games(self):
        """Marks status for stale games as `stale`

        If any games marked `active` has one or more players who no
        longer has a `current_game_id` matching the game's `game_id`,
        the game will have its status changed to `stale`
        """
        games = self.db['games']
        player_table = self.db['players']

        games_to_delete = []
        for game in games:
            players = self.get_players_for_game(game['game_id'])
            for p in players:
                _p = player_table.find_one(name=p)
                if all([_p['current_game_id'] != game['game_id'],
                        game['status'] == "active"]):
                    games_to_delete.append(game['game_id'])
                    break

        for game_id in games_to_delete:
            games.update(dict(game_id=game_id, status="stale"), ['game_id'])
            logging.info("Marked {} as stale.".format(game_id))
            # If we wanted to delete games instead of simply marking them
            #   stale, we would do this:
            # games.delete(game_id=game_id)

    def create_room(self, room_name, password, owner):
        """Create a new room `room_name`

        Adds entry for room `room_name` to the database.
        :raises APIError: If a room with `room_name` has already
            been created.
        """
        rtable = self.db['rooms']
        api_assert(not rtable.find_one(name=room_name), 409,
                   log_message="Room with name `{}` already exists.".format(
                       room_name))

        rtable.insert(
            {
                "name": room_name,
                "password": password,
                "owner": owner,
                "current_players": ""
            }
        )

    def __get_player(self, player_name):
        ptable = self.db['players']
        player = ptable.find_one(name=player_name)
        return ptable, player

    def _get_player(self, player_name):
        ptable, player = self.__get_player(player_name)
        api_assert(player, 409,
                   log_message="No user {} exists.".format(player_name))
        return ptable, player

    def __get_room(self, room_name):
        rtable = self.db['rooms']
        room = rtable.find_one(name=room_name)
        return rtable, room

    def _get_room(self, room_name):
        rtable, room = self.__get_room(room_name)
        api_assert(room, 409,
                   log_message="No room {} exists".format(room_name))
        return rtable, room

    def join_room(self, room_name, password, player_name):
        """Join room `room_name`

        Updates `current_players` entry for room `room_name` with
        player `player_name` to the database.

        :raises APIError: If a room with `room_name` does not exist;
            or if the password is incorrect for room `room_name`, or if player
            `player_name` does not exist
        """
        rtable = self.db['rooms']
        room = rtable.find_one(name=room_name)
        api_assert(room, 409,
                   log_message="No room {} exists".format(room_name))
        api_assert(password == room['password'], 403,
                   log_message="Bad password for room `{}`.".format(room_name))

        ptable, player = self._get_player(player_name)

        api_assert(
            player_name not in listify_string(str, room['current_players']),
            409,
            log_message="Player `{}` already in room `{}`".format(
                player_name, room_name)
        )

        rtable.update(
            {
                "name": room_name,
                "current_players": stringify_list(
                    listify_string(str, room['current_players']) +
                    [player_name]
                )
            },
            ['name']
        )

        ptable.update(
            {
                "name": player_name,
                "current_room": room_name
            },
            ['name']
        )

    def leave_room(self, player_name):
        ptable, player = self._get_player(player_name)
        room_name = player["current_room"]
        api_assert(
            room_name, 409,
            "`{}` is currently not in a room.".format(player_name)
        )

        rtable = self.db['rooms']
        room = rtable.find_one(name=room_name)

        api_assert(
            room["owner"] != player_name,
            409,
            log_message=(
                "Owners cannot leave their rooms (you are the owner"
                " of this room). Please retire the room if you wish to leave"
                " it."
            )
        )

        ptable.update(
            {
                "name": player_name,
                "current_room": None
            },
            ['name']
        )

        rtable.update(
            {
                "name": room_name,
                "current_players": stringify_list(
                    list(set(listify_string(str, room['current_players'])) -
                         set([player_name]))
                )
            },
            ['name']
        )

        return room_name

    def delete_room(self, player_name):
        ptable, player = self._get_player(player_name)
        room_name = player["current_room"]
        api_assert(
            room_name, 409,
            "`{}` is currently not in a room.".format(player_name)
        )

        rtable = self.db['rooms']
        room = rtable.find_one(name=room_name)

        api_assert(
            room["owner"] == player_name,
            403,
            log_message="You must own the room if you want to destroy it."
        )

        # Set each player's room to None, then delete the room
        for p in listify_string(str, room["current_players"]):
            ptable.update(
                {
                    "name": p,
                    "current_room": None
                },
                ['name']
            )
        rtable.delete(name=room_name)

        return room_name

    def player_info(self, player_name):
        ptable, player = self._get_player(player_name)
        res = dict(player)
        # Return balls as a list
        res["balls"] = listify_string(int, res["balls"])
        res.pop("password")  # Redact password
        res.pop("salt")  # Redact salt
        res.pop("id")  # Players don't care about this
        return res

    def get_player_room(self, player_name):
        """:returns: Name of the room `player_name` is in, or None"""
        # rtable = self.db['rooms']
        # for room in rtable.all():
        #     if player_name in listify_string(str, room['current_players']):
        #         return room["name"]
        # return None
        ptable, player = self._get_player(player_name)
        player_room = player["current_room"]
        return player_room if player_room else None

    def list_rooms(self):
        """List rooms

        :returns: List of all created rooms
        :rtype: list
        """
        return [
            {
                "name": r["name"],
                "pwd_req": bool(r["password"])
            } for r in self.db['rooms'].all()
        ]

    def get_owned_room(self, player_name):
        """:returns: name of room owned by `player_name` else None"""
        rtable = self.db['rooms']
        room = rtable.find_one(owner=player_name)
        return room["name"] if room else None

    def get_players_in_room(self, room_name):
        """
        :returns: Players participating in game `game_id`
        :rtype: [str, ...]
        """
        rtable, room = self._get_room(room_name)
        players = listify_string(str, room['current_players'])
        return players

    def leave_game(self, player_name):
        """Remove `player_name` from current game
        :returns: ID of game that `player_name` left
        """
        ptable, player = self._get_player(player_name)
        game_id = player["current_game_id"]
        api_assert(game_id, 409,
                   log_message="You are not currently in a game.")

        gtable = self.db["games"]
        game = self.db["games"].find_one(game_id=game_id)
        if not game:
            raise AttributeError("Expected game not found.")

        # Get remaining set of players
        rem_players = list(
            set(listify_string(str, game['players'])) -
            set([player_name])
        )
        # Set new gamemaster
        if not rem_players:
            new_gamemaster = None
        else:
            # If gamemaster is leaving, assign to a random player
            if game["gamemaster"] == player_name:
                new_gamemaster = choice(rem_players)
            else:
                new_gamemaster = game["gamemaster"]

        # Remove player from game's list of players and set player's
        #   current_game_id to None
        # Add player's remaining balls to game's unclaimed set
        gtable.update(
            {
                "players": stringify_list(rem_players),
                "game_id": game_id,
                "unclaimed_balls": game["unclaimed_balls"] + "," + player["balls"],
                "gamemaster": new_gamemaster
            },
            ["game_id"],
        )
        ptable.update(
            {
                "current_game_id": None,
                "name": player_name,
                "balls": ""
            },
            ["name"]
        )

        return game_id
