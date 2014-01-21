from cutthroat.handlers import ViewHandler


class Login(ViewHandler):

    """Handle authentication"""

    def get(self):
        self.write('<html><body><form action="{}" method="post">'
                   'Name: <input type="text" name="name"><br>'
                   'Password: <input type="password" name="password"><br>'
                   '<input type="submit" value="Sign in">'
                   '</form></body></html>'.format(self.settings['login_url']))
