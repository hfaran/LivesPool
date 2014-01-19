import math
from random import shuffle
from itertools import chain


TOTAL_NUM_BALLS = 15


def generate_balls(num):
    """:returns: list of balls from 1 through num"""
    return map(lambda x: x + 1, range(num))


class Player(object):

    """Cutthroat Player"""

    def __init__(self, balls):
        self.init_balls = balls[:]
        self.balls = balls

    @property
    def alive(self):
        """Is this player alive?"""
        return True if self.balls else False


class Game(object):

    """Cutthroat Game"""

    def __init__(self, nbpp, player_names):
        player_names = player_names[:]
        nplayers = len(player_names)

        # Make sure values make sense
        if nbpp * nplayers > TOTAL_NUM_BALLS:
            raise ArithmeticError("There are literally not enough balls to "
                                  "accomodate the game you are trying to "
                                  "create.")

        balls = generate_balls(TOTAL_NUM_BALLS)
        shuffle(balls)

        self.players = {}
        for i in xrange(nplayers):
            _balls = []
            for i in xrange(nbpp):
                _balls.append(balls.pop())
            self.players[player_names.pop()] = Player(_balls)

        self.unclaimed_balls = balls[:]

    @property
    def over(self):
        """Is the game over?"""
        return True if len(
            [True for p in self.players.values() if p.alive]
        ) <= 1 else False

    def balls_on_table(self):
        """:returns: list of balls on the table"""
        return list(
            chain(*[p.balls for p in self.players.values()])
        ) + self.unclaimed_balls

    def balls_sunk(self):
        """:returns: list of balls sunk"""
        return list(
            set(generate_balls(TOTAL_NUM_BALLS)) - set(self.balls_on_table())
        )

    def sink_ball(self, ball):
        """Sink ball `ball`

        Sink `ball`, i.e., remove from the player whose it is or from
        `unclaimed_balls` if it is no player's
        """
        # If ball is already sunk, do nothing
        if ball not in self.balls_on_table():
            return

        for p in self.players.values():
            if ball in p.balls:
                p.balls.remove(ball)
                break
        else:
            self.unclaimed_balls.remove(ball)

    def return_ball(self, ball):
        """Return ball `ball` to the table

        Return `ball`, i.e., add back to the player whose it was originally
        """
        # If ball was never sunk, do nothing
        if ball in self.balls_on_table():
            return

        for p in self.players.values()
            if ball in p.init_balls:
                p.balls.append(ball)
                break
        else:
            self.unclaimed_balls.balls.append(ball)
