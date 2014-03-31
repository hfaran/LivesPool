import bcrypt

from tornado.options import options
from tornado.web import authenticated
from tornado_json.exceptions import APIError
from tornado_json import schema

from cutthroat.handlers import APIHandler
from cutthroat.common import get_player


class Login(APIHandler):

    """Handle authentication"""

    @schema.validate(
        input_schema={
            "required": ["username", "password"],
            "type": "object",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
        },
        output_schema={
            "type": "object",
            "properties": {
                "username": {"type": "string"}
            }
        },
    )
    def post(self):
        """POST the required credentials to get back a cookie

        * `username`: Username
        * `password`: Password
        """
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

    @schema.validate(
        output_schema={"type": "string"}
    )
    def get(self):
        """GET to check if authenticated.

        Should be obvious from status code (403 vs. 200).
        """
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

    @authenticated
    @schema.validate(
        output_schema={"type": "string"},
    )
    def delete(self):
        """DELETE to clear cookie for current user."""
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
