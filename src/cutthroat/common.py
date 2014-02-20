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
