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

    def create_game(game_id, players, unclaimed_balls):
        table = self.db['games']
        table.insert(
            {
                "game_id": game_id,
                "players": ",".join(players.keys()),
                "unclaimed_balls": ",".join(unclaimed_balls)
            }
        )

        table = self.db['players']
        for name, balls in players.iteritems():
            table.update(
                {
                    "name": name,
                    "current_game_id": game_id,
                    "balls": ",".join(balls)
                },
                ['name']
            )

    def create_player(player_name):
        table = self.db['player']
        table.insert(
                {
                    "name": name,
                }
            )