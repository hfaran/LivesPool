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