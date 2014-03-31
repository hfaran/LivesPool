from itertools import chain
from tornado_json.exceptions import APIError

from cutthroat.db2 import Player, Game, Room, NotFoundError


def get_player(db, player_name, err_code=409):
    """Get player ``player_name``

    :returns: Player with ``player_name``
    :raises APIError: If no Player with ``player_name`` found
    """
    try:
        player = Player(db, "name", player_name)
    except NotFoundError:
        raise APIError(
            err_code,
            log_message="No user {} exists.".format(player_name)
        )
    return player


def get_room(db, room_name, err_code=409):
    """Get room ``room_name``

    :returns: Room with ``room_name``
    :raises APIError: If no Room with ``room_name`` found
    """
    try:
        room = Room(db, "name", room_name)
    except NotFoundError:
        raise APIError(
            err_code,
            log_message="No room {} exists.".format(room_name)
        )
    return room


def get_game(db, game_id, err_code=409):
    """Get game with ``game_id``

    :returns: Game with game_id ``game_id``
    :raises APIError: If no Game with game_id ``game_id`` found
    """
    try:
        game = Game(db, "game_id", game_id)
    except NotFoundError:
        raise APIError(
            err_code,
            log_message="No game with game_id {} exists.".format(game_id)
        )
    return game


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


def get_game_winner(db, game_id):
    """Get winner of game ``game_id``

    :returns: Game winner if there is one otherwise empty string
    :rtype: str
    """
    game = get_game(db, game_id)
    players_with_balls = []
    for pname in game["players"]:
        p = get_player(db, pname)
        if p["balls"]:
            players_with_balls.append(pname)
        if len(players_with_balls) > 1:
            winner = ""
            break
    else:
        if players_with_balls:
            winner = players_with_balls[0]
        else:
            raise APIError(
                409,
                log_message="No player currently has balls on the table."
            )

    return winner


# Periodic Callbacks ###################################################
