import tornado.ioloop
from tornado_json.routes import get_routes
from tornado_json.application import Application

from cutthroat import api


def main():
    routes = get_routes(api)

    application = Application(routes=routes, settings={})

    application.listen(7777)
    tornado.ioloop.IOLoop.instance().start()

    self.games = {}


if __name__ == '__main__':
    main()
