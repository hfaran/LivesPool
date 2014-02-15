from tornado.testing import AsyncHTTPSTestCase
from tornado_json.application import Application

from cutthroat import routes as mod_routes
from cutthroat import db


class APIFunctionalTest(AsyncHTTPSTestCase):
    def get_app(self):
        settings = dict(
            cookie_secret="I am a secret cookie.",
        )
        return Application(
            routes=mod_routes.assemble_routes(),
            settings=settings,
            db_conn=db.Connection("/tmp/cutthroat_test.db")
        )



    def test_full_game_run(self):
