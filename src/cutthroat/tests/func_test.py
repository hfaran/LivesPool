import json

from tornado.testing import AsyncHTTPSTestCase
from tornado.options import define
from tornado_json.application import Application

from cutthroat import routes as mod_routes
from cutthroat import db


def jd(obj):
    return json.dumps(obj)


class APIFunctionalTest(AsyncHTTPSTestCase):

    def get_app(self):
        define("session_timeout_days", 1)
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

    def _create_room(self, cookies, room_name, password=None):
        data = dict(roomname=room_name)
        if password:
            data["password"] = password
        return self.fetch(
            "/api/room/createroom",
            method="POST",
            data=jd(data),
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
            data=jd(data),
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
            data=jd(dict(nbpp=nbpp)),
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
            data=jd(dict(ball=ball)),
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
