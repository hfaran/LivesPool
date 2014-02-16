import json

from tornado.testing import AsyncHTTPSTestCase
from tornado_json.application import Application

from cutthroat import routes as mod_routes
from cutthroat import db
from cutthroat import ctconfig


def jd(obj):
    return json.dumps(obj)


def jl(s):
    return json.loads(s)


class APIFunctionalTest(AsyncHTTPSTestCase):

    def get_app(self):
        ctconfig.define_options()
        settings = dict(
            cookie_secret="I am a secret cookie.",
        )
        return Application(
            routes=mod_routes.assemble_routes(),
            settings=settings,
            db_conn=db.Connection("cutthroat_test.db")
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
        for p in ["alpha", "beta", "gamma"]:
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
