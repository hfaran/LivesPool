from cutthroat.handlers import APIHandler

class Login(APIHandler):

    """Handle authentication"""

    def post(self):
        player_name = self.get_argument("name")
        password = self.get_argument("password")

        if self.db_conn.auth_user(player_name, password):
            self.set_secure_cookie("user", player_name)
            self.redirect("http://www.google.com")
        else:
            self.write("Bad username/password combo."
                       "Click <a href=\"{}\">here</a> to try again".
                       format(self.settings['login_url']))
