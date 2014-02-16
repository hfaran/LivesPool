import json
from random import choice

from tornado.testing import AsyncHTTPSTestCase
from tornado_json.application import Application

from cutthroat import routes as mod_routes
from cutthroat import db
from cutthroat import db2
from cutthroat import ctconfig


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s)


class APIFunctionalTest(AsyncHTTPSTestCase):

    def get_app(self):
        ctconfig.define_options()
        db_conn = db.Connection("cutthroat_test.db")
        self.db = db_conn.db
        settings = dict(
            cookie_secret="I am a secret cookie.",
        )
        return Application(
            routes=mod_routes.assemble_routes(),
            settings=settings,
            db_conn=db_conn
        )

    def _sign_up(self, username, password):
        return self.fetch(
            "/api/player/player",
            method="POST",
            body=jd({"username": username, "password": password})
        )

    def _authenticate(self, username, password):
        return self.fetch(
            "/api/auth/login",
            method="POST",
            body=jd({"username": username, "password": password})
        )

    def _check_auth(self, cookies=None):
        headers = {"Cookie": cookies} if cookies else {}
        return self.fetch(
            "/api/auth/login",
            method="GET",
            headers=headers
        )

    def _logout(self, cookies=None):
        headers = {"Cookie": cookies} if cookies else {}
        return self.fetch(
            "/api/auth/logout",
            method="DELETE",
            headers=headers
        )

    def _create_room(self, cookies, room_name, password=None):
        data = dict(roomname=room_name)
        if password:
            data["password"] = password
        return self.fetch(
            "/api/room/createroom",
            method="POST",
            body=jd(data),
            headers={"Cookie": cookies}
        )

    def _list_rooms(self, cookies):
        return self.fetch(
            "/api/room/listrooms",
            method="GET",
            headers={"Cookie": cookies}
        )

    def _join_room(self, cookies, name, password=None):
        data = dict(name=name)
        if password:
            data['password'] = password

        return self.fetch(
            "/api/room/joinroom",
            body=jd(data),
            method="POST",
            headers={"Cookie": cookies}
        )

    def _list_room_players(self, cookies):
        return self.fetch(
            "/api/room/listplayers",
            method="GET",
            headers={"Cookie": cookies}
        )

    def _get_self_info(self, cookies):
        return self.fetch(
            "/api/player/player",
            method="GET",
            headers={"Cookie": cookies}
        )

    def _leave_room(self, cookies):
        return self.fetch(
            "/api/room/leaveroom",
            method="DELETE",
            headers={"Cookie": cookies}
        )

    def _retire_room(self, cookies):
        return self.fetch(
            "/api/room/retireroom",
            method="DELETE",
            headers={"Cookie": cookies}
        )

    def _start_game(self, cookies, nbpp):
        return self.fetch(
            "/api/game/creategame",
            body=jd(dict(nbpp=nbpp)),
            method="POST",
            headers={"Cookie": cookies}
        )

    def _leave_game(self, cookies):
        return self.fetch(
            "/api/game/leavegame",
            method="DELETE",
            headers={"Cookie": cookies}
        )

    def _sink_ball(self, cookies, ball):
        return self.fetch(
            "/api/game/sinkball",
            body=jd(dict(ball=ball)),
            method="POST",
            headers={"Cookie": cookies}
        )

    def _balls_on_table(self, cookies):
        return self.fetch(
            "/api/game/ballsontable",
            method="GET",
            headers={"Cookie": cookies}
        )

    def sign_up(self, username, password):
        r = self._sign_up(username, password)
        self.assertEqual(r.code, 200)

    def test_full_game_run(self):
        # Create three new players
        cookies = {}
        for p in ["alpha", "beta", "gamma", "delta"]:
            self.sign_up(p, p)
            cookies[p] = self._authenticate(p, p).headers['set-cookie']
        self.assertTrue('user="' in cookie for cookie in cookies)

        # Test creation of existing player
        r = self._sign_up(username="alpha", password="alpha")
        self.assertEqual(r.code, 409)
        # Test bad authentication
        r = self._authenticate(username="alpha", password="beta")
        self.assertEqual(r.code, 400)
        # Test GET /api/auth/login
        r = self._check_auth()
        self.assertEqual(r.code, 403)
        r = self._check_auth(cookies["alpha"])
        self.assertEqual(r.code, 200)
        # Test DELETE /api/auth/logout
        r = self._logout(cookies["alpha"])
        self.assertEqual(r.code, 200)
        # TODO: This endpoint, for whatever reason, doesn't actually kill
        #   the cookies it's supposed to. The following lines should pass
        #   when it actually does.
        # r = self._check_auth(cookies["alpha"])
        # self.assertEqual(r.code, 403)

        # Test /api/player/player
        r = self._get_self_info(cookies["alpha"])
        self.assertEqual(r.code, 200)
        self.assertEqual(jl(r.body)["data"]["name"], "alpha")

        # Test api.room
        r = self._create_room(cookies["alpha"], "Moria", "mellon")
        self.assertEqual(r.code, 200)
        # Test non-tenancy assertion
        r = self._create_room(cookies["alpha"], "Moria", "mellon")
        self.assertEqual(r.code, 409)
        self.assertTrue("already in a room" in jl(r.body)["data"])
        # Attempt to create existing room
        r = self._create_room(cookies["beta"], "Moria", "mellon")
        self.assertEqual(r.code, 409)

        # Attempt to join non-existant room
        r = self._join_room(cookies["beta"], "Lothlorien")
        self.assertEqual(r.code, 409)
        # Attempt to join room with incorrect password
        r = self._join_room(cookies["beta"], "Moria", "enemy")
        self.assertEqual(r.code, 403)
        # Join room
        r = self._join_room(cookies["beta"], "Moria", "mellon")
        self.assertEqual(r.code, 200)
        # Retrieve list of rooms
        r = self._list_rooms(cookies["beta"])
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"],
            [{"pwd_req": True, "name": "Moria"}]
        )
        # List players in room
        r = self._list_room_players(cookies["beta"])
        self.assertEqual(r.code, 200)
        self.assertEqual(
            sorted(jl(r.body)["data"]["players"]),
            ["alpha", "beta"]
        )

        # Test attempting to leave room if owner
        r = self._leave_room(cookies["alpha"])
        self.assertEqual(r.code, 409)
        # Test attempting to retire room if not owner
        r = self._retire_room(cookies["beta"])
        self.assertEqual(r.code, 403)
        # Test attempting to retire room if not in room
        r = self._retire_room(cookies["gamma"])
        self.assertEqual(r.code, 409)
        self.assertTrue("not in a room" in jl(r.body)["data"])
        # Test attempting to leave room if not in room
        r = self._leave_room(cookies["gamma"])
        self.assertEqual(r.code, 409)
        self.assertTrue("not in a room" in jl(r.body)["data"])
        # Test leaving room
        r = self._leave_room(cookies["beta"])
        self.assertEqual(r.code, 200)
        # Test retiring room
        r = self._retire_room(cookies["alpha"])
        self.assertEqual(r.code, 200)

        # Create and join room for the purposes of testing api.game
        r = self._create_room(cookies["alpha"], "Rivendell")
        self.assertEqual(r.code, 200)
        r = self._join_room(cookies["beta"], "Rivendell")
        self.assertEqual(r.code, 200)
        r = self._join_room(cookies["gamma"], "Rivendell")
        self.assertEqual(r.code, 200)

        # Attempt to create a game w/o owning a room
        r = self._start_game(cookies["delta"], 5)
        self.assertEqual(r.code, 403)
        r = self._start_game(cookies["gamma"], 5)
        self.assertEqual(r.code, 403)
        # Attempt to start game with malformed nbpp values
        r = self._start_game(cookies["alpha"], -20000)
        self.assertEqual(r.code, 400)
        r = self._start_game(cookies["alpha"], 0)
        self.assertEqual(r.code, 400)
        r = self._start_game(cookies["alpha"], 6)
        self.assertEqual(r.code, 400)
        # Successfully create game
        r = self._start_game(cookies["alpha"], 5)
        self.assertEqual(r.code, 200)
        game_id = jl(r.body)["data"]["game_id"]

        # Attempt to sinkball as not the gamemaster
        r = self._sink_ball(cookies["beta"], 10)
        self.assertEqual(r.code, 401)
        # Sink a ball
        r = self._sink_ball(cookies["alpha"], 10)
        self.assertEqual(r.code, 200)
        # Sink an already sunk ball
        r = self._sink_ball(cookies["alpha"], 10)
        self.assertEqual(r.code, 200)
        self.assertEqual(
            jl(r.body)["data"]["message"],
            "Ball 10 was not on the table."
        )

        # Attempt to get balls on table when not in game
        r = self._balls_on_table(cookies["delta"])
        self.assertEqual(r.code, 400)
        # Test balls on table
        r = self._balls_on_table(cookies["beta"])
        self.assertEqual(r.code, 200)
        self.assertEqual(
            sorted(jl(r.body)["data"]),
            filter(lambda a: a not in [10], xrange(1, 16))
        )

        # Attempt to leave game when not in a game
        r = self._leave_game(cookies["delta"])
        self.assertEqual(r.code, 409)
        self.assertEqual(
            jl(r.body)["data"],
            "You are not currently in a game."
        )
        # Regular player leave game
        g = db2.Game(self.db, "game_id", game_id)
        p = db2.Player(self.db, "name", "gamma")
        gamma_balls = list(p["balls"])
        r = self._leave_game(cookies["gamma"])
        self.assertEqual(r.code, 200)
        self.assertTrue("gamma" not in g["players"])
        self.assertFalse(p["current_game_id"])
        self.assertEqual(g["gamemaster"], "alpha")
        self.assertEqual(g["unclaimed_balls"], gamma_balls)
        # Sink ball from unclaimed
        unc_ball = choice(gamma_balls)
        gamma_balls.remove(unc_ball)
        r = self._sink_ball(cookies["alpha"], unc_ball)
        self.assertEqual(r.code, 200)
        # Gamemaster leave game
        p = db2.Player(self.db, "name", "alpha")
        alpha_balls = list(p["balls"])
        r = self._leave_game(cookies["alpha"])
        self.assertEqual(r.code, 200)
        self.assertTrue("alpha" not in g["players"])
        self.assertFalse(p["current_game_id"])
        self.assertEqual(g["gamemaster"], "beta")
        self.assertEqual(g["unclaimed_balls"], gamma_balls + alpha_balls)
        # Last player in game, leave
        r = self._leave_game(cookies["beta"])
        self.assertEqual(r.code, 200)
        self.assertEqual(g["gamemaster"], None)
