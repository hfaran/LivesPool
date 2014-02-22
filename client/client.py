import logging
import requests
import json
import getpass

DEBUG = True


class AuthenticationError(Exception):

    """AuthenticationError"""


class CutthroatAPI(object):

    """CutthroatAPI

    >>> from client import CutthroatAPI
    >>> c = CutthroatAPI()
    Username: ...
    Password: ...
    >>> c.list_rooms()
    ...
    """

    def __init__(self, base_url="http://localhost:8888",
                 signup=False, username=None):
        self.base_url = base_url

        self.username = username if username else raw_input("Username: ")
        password = getpass.getpass()
        if signup:
            self._sign_up(self.username, password)
        self.cookies = self._authenticate(self.username, password)

        info = self.get_self_info()["data"]
        self.room = info.get("current_room") if \
            info.get("current_room") else None
        self.game = info.get("current_game_id") if \
            info.get("current_game_id") else None

    def _sign_up(self, username, password):
        """Sign up with `username` and `password`"""
        r = requests.post(
            self.base_url + "/api/player/player",
            data=json.dumps({
                "username": username,
                "password": password
            })
        )
        if r.status_code == 200:
            return r.json()
        else:
            raise AuthenticationError(r.json()["data"])

    def _authenticate(self, username, password):
        """Login with `username` and `password`"""
        r = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps({
                "username": username,
                "password": password
            })
        )
        if DEBUG:
            print("{}\n{}".format(r, r.json()))
        if r.status_code == 200:
            return r.cookies
        else:
            raise AuthenticationError(r.json().get("data"))

    def create_room(self):
        roomname = raw_input("Name of the room: ")
        password = raw_input("(Optional) Password to the room if you "
                             "wish to keep entry restricted to players who "
                             "know the password: ")

        data = dict(roomname=roomname)
        if password:
            data["password"] = password

        r = requests.post(
            self.base_url + "/api/room/createroom",
            data=json.dumps(data),
            cookies=self.cookies
        )
        logging.info("{}\n{}".format(r, r.json()))

        if r.status_code == 200:
            self.join_room(roomname, password)
        return r.json()

    def list_rooms(self):
        r = requests.get(
            self.base_url + "/api/room/listrooms",
            cookies=self.cookies
        )
        if r.status_code is 200:
            return r.json()[u"data"]
        else:
            return r.json()

    def join_room(self, name=None, password=None):
        if not name:
            name = raw_input("Name of the room: ")
        if not password:
            password = raw_input(
                "(Optional) Password to the room if it has one: "
            )
        player = self.username

        data = dict(name=name, player=player)
        if password:
            data["password"] = password

        r = requests.post(
            self.base_url + "/api/room/joinroom",
            data=json.dumps(data),
            cookies=self.cookies
        )
        logging.info("{}\n{}".format(r, r.json()))

        if r.status_code == 200:
            self.room = name
        return r.json()

    def list_room_players(self):
        r = requests.get(
            self.base_url + "/api/room/listplayers",
            cookies=self.cookies
        )
        return r.json()

    def get_self_info(self):
        r = requests.get(
            self.base_url + "/api/player/player",
            cookies=self.cookies
        )
        return r.json()

    def leave_room(self):
        r = requests.delete(
            self.base_url + "/api/room/leaveroom",
            cookies=self.cookies
        )
        if r.status_code == 200:
            self.room = None
        return r.json()

    def start_game(self, nbpp=None):
        if nbpp is None:
            nbpp = int(raw_input("Number of balls per player? "))
        r = requests.post(
            self.base_url + "/api/game/creategame",
            data=json.dumps({"nbpp": nbpp}),
            cookies=self.cookies
        )
        if r.status_code == 200:
            self.game = r.json()["data"]["game_id"]
            self.room = None
        return r.json()

    def leave_game(self):
        r = requests.delete(
            self.base_url + "/api/game/leavegame",
            cookies=self.cookies
        )
        if r.status_code == 200:
            self.game = None
        return r.json()

    def toggle_ball(self, ball=None):
        if ball is None:
            ball = int(raw_input("Which ball to toggle? "))
        r = requests.post(
            self.base_url + "/api/game/toggleball",
            data=json.dumps({"ball": ball}),
            cookies=self.cookies
        )
        return r.json()

    def game_state(self):
        r = requests.get(
            self.base_url + "/api/game/gamestate",
            cookies=self.cookies
        )
        return r.json()
