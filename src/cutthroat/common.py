from itertools import chain
from tornado_json.utils import APIError

from cutthroat.db2 import Player, Game, Room, NotFoundError


def get_player(db, player_name):
    try:
        player = Player(db, "name", player_name)
    except NotFoundError:
        raise APIError(
            409,
            log_message="No user {} exists.".format(player_name)
        )

    return player


def get_room(db, room_name):
    try:
        room = Room(db, "name", room_name)
    except NotFoundError:
        raise APIError(
            409,
            log_message="No room {} exists.".format(room_name)
        )

    return room


def get_balls_on_table(db, game_id):
    """
    :returns: Balls currently on the table for game `game_id`
    :rtype: [int, ...]
    """
    game = Game(db, "game_id", game_id)
    players = game["players"]
    unclaimed_balls = game["unclaimed_balls"]

    return list(
        chain(*[get_player(db, p)["balls"] for p in players])
    ) + unclaimed_balls


# Periodic Callbacks ###################################################
