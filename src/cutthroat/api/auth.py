import bcrypt

from tornado.options import options
from tornado.web import authenticated
from tornado_json.utils import io_schema, APIError

from cutthroat.handlers import APIHandler
from cutthroat.common import get_player


class Login(APIHandler):

    """Handle authentication"""

    apid = {}
    apid["post"] = {
        "input_schema": {
            "required": ["username", "password"],
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        },
        "doc": """
POST the required credentials to get back a cookie

* `username`: Username
* `password`: Password
"""
    }
    apid["get"] = {
        "input_schema": None,
        "output_schema": {"type": "string"},
        "doc": """
GET to check if authenticated. Should be obvious from status code (403 vs. 200).
"""
    }

    @io_schema
    def post(self):
        player_name = self.body["username"]
        password = self.body["password"]
        player = get_player(self.db_conn, player_name, err_code=400)

        # Check if the given password hashed with the player's known
        #   salt matches the stored password
        password_match = bcrypt.hashpw(
            str(password), str(player["salt"])
        ) == player['password']
        if password_match:
            self.set_secure_cookie(
                "user", player_name, options.session_timeout_days
            )
            return {"username": player_name}
        else:
            raise APIError(
                400,
                log_message="Bad username/password combo"
            )

    @io_schema
    def get(self):
        if not self.get_current_user():
            raise APIError(
                403,
                log_message="Please post to {} to get a cookie".format(
                    "/api/auth/login")
            )
        else:
            return "You are already logged in."


class Logout(APIHandler):

    """Logout"""

    apid = {}
    apid["delete"] = {
        "input_schema": None,
        "output_schema": {"type": "string"},
    "doc": """
DELETE to clear cookie for current user.
"""
    }

    @authenticated
    @io_schema
    def delete(self):
        # So this doesn't actually with the CLI client...
        #  can still authenticate with old cookie. Maybe we'll have
        #  better luck with browser? UPDATE: Works in browser.
        # Apparently if you set `expires_days` to None, it becomes
        #  a session cookie which will be gone when the player closes
        #  their browser, so if all else fails, we can just have an implicit
        #  logout which occurs by closing the window. In some ways,
        #  that's a much better way to log out that to have an explicit
        #  button anyways.
        self.clear_cookie("user")
        return "Logout was successful."
