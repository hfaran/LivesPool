from itertools import chain

from tornado.options import options
from tornado_json.db import MySQLConnection


def stringify_list(l):
    return ",".join(map(str, l))


def listify_string(func, s):
    if not s:
        return []
    else:
        return map(func, s.split(","))


class Connection(object):

    def __init__(self):
        conn = MySQLConnection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password,
        )
        self.generic_query = conn.generic_query
        self.db = conn._db_dataset

    def create_game(self, game_id, players, unclaimed_balls, password):
        table = self.db['games']
        table.insert(
            {
                "game_id": game_id,
                "players": stringify_list(players.keys()),
                "unclaimed_balls": stringify_list(unclaimed_balls),
                "password": password
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

    def create_player(self, player_name):
        table = self.db['players']
        table.insert(
            {
                "name": player_name,
            }
        )

    def get_balls_for_player(self, player_name):
        table = self.db['players']
        return listify_string(int, table.find_one(name=player_name)['balls'])

    def remove_ball_for_player(self, player_name, ball):
        balls = self.get_balls_for_player(player_name)
        balls.remove(ball)

        table = self.db['players']
        table.update(dict(name=player_name, balls=stringify_list(balls)),
                     ['name'])

    def remove_ball_from_unclaimed(self, game_id, ball):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        unclaimed_balls = listify_string(int, game['unclaimed_balls'])
        unclaimed_balls.remove(ball)
        table.update(dict(game_id=game_id, unclaimed_balls=stringify_list(
            unclaimed_balls)),
            ['game_id']
        )

    def get_players_for_game(self, game_id):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        players = listify_string(str, game['players'])
        return players

    def get_balls_on_table(self, game_id):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        players = listify_string(str, game['players'])
        unclaimed_balls = listify_string(int, game['unclaimed_balls'])

        return list(
            chain(*[self.get_balls_for_player(p) for p in players])
        ) + unclaimed_balls

    def auth_game_update_request(self, game_id, password):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        return game['password'] == password
