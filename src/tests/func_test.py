import json

from tornado.testing import AsyncHTTPSTestCase
from tornado_json.application import Application

from cutthroat import routes as mod_routes
from cutthroat import db


def jd(obj):
    return json.dumps(obj)


class APIFunctionalTest(AsyncHTTPSTestCase):
    def get_app(self):
        settings = dict(
            cookie_secret="I am a secret cookie.",
        )
        return Application(
            routes=mod_routes.assemble_routes(),
            settings=settings,
            db_conn=db.Connection("cutthroat_test.db")
        )

    def sign_up(self, username, password):
        return self.fetch(
            "/api/player/player",
            method="POST",
            body=jd({"username": username, "password": password})
        )

    def authenticate(self, username, password):
        return self.fetch(
            "/api/auth/login",
            method="POST",
            body=jd({"username": username, "password": password})
        )

    def create_room(self, room_name, password=None):
        data=dict(roomname=room_name)
        if password:
            data["password"] = password
        return self.fetch(
            "/api/room/createroom",
            method="POST",
            data=jd(data)
        )

    def list_rooms(self):
        return self.fetch(
            "/api/room/listrooms",
            method="GET"
        )

    def join_room(self, name, password=None):
        data=dict(name=name)
        if password:
            data['password'] = password

        return self.fetch(
            "/api/room/joinroom",
            data=jd(data),
            method="POST"
        )

    def list_room_players(self):
        return self.fetch(
            "/api/room/listplayers",
            method="GET"
        )

    def get_self_info(self):
        return self.fetch(
            "/api/player/player",
            method="GET"
        )

    def leave_room(self):
        return self.fetch(
            "/api/room/leaveroom",
            method="DELETE"
        )

    def retire_room(self):
        return self.fetch(
            "/api/room/retireroom",
            method="DELETE"
        )

    def start_game(self, nbpp):
        return self.fetch(
            "/api/game/creategame",
            data=jd(dict(nbpp=nbpp)),
            method="POST"
        )

    def leave_game(self):
        return self.fetch(
            "/api/game/leavegame",
            method="DELETE"
        )

    def sink_ball(self, ball):
        return self.fetch(
            "/api/game/sinkball",
            data=jd(dict(ball=ball)),
            method="POST"
        )

    def balls_on_table(self):
        return self.fetch(
            "/api/game/ballsontable",
            method="GET"
        )

    def test_full_game_run(self):
        pass
