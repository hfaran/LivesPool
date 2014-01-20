from itertools import chain

from tornado.options import options
from tornado_json.db import MySQLConnection


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

    def create_game(self, game_id, players, unclaimed_balls):
        table = self.db['games']
        table.insert(
            {
                "game_id": game_id,
                "players": ",".join(players.keys()),
                "unclaimed_balls": ",".join(map(str, unclaimed_balls))
            }
        )

        table = self.db['players']
        for name, balls in players.iteritems():
            table.update(
                {
                    "name": name,
                    "current_game_id": game_id,
                    "balls": ",".join(map(str, balls))
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
        return map(int, table.find_one(name=player_name)['balls'])

    def get_balls_on_table(self, game_id):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        players = game['players'].split(",")
        unclaimed_balls = map(int, game['unclaimed_balls'].split(","))

        return list(
            chain(*[self.get_balls_for_player(p) for p in players])
        ) + unclaimed_balls

    def auth_game_update_request(self, game_id, password):
        table = self.db['games']
        game = table.find_one(game_id=game_id)
        return game['password'] == password
