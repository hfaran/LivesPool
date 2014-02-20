import logging
import dataset


class Connection(object):

    """Connection to cutthroat MySQL database"""

    def __init__(self, db_path):
        self.db = dataset.connect('sqlite:///{}'.format(db_path))

    # TODO: re-evaluate what this function will actually do
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
