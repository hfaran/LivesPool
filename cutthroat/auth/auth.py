from cutthroat.handlers import APIHandler, ViewHandler


class Login(ViewHandler):

    """Handle authentication"""

    def get(self):
        self.write('<html><body><form action="{}" method="post">'
                   'Name: <input type="text" name="name">'
                   'Password: <input type="password" name="password">'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>'.format(self.settings['login_url']))

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
