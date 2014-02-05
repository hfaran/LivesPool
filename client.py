import logging
import requests
import json
import getpass

class AuthenticationError(Exception):

    """AuthenticationError"""

class CutthroatAPI(object):
    """CutthroatAPI"""
    def __init__(self, base_url="http://localhost:8888", username=None):
        self.base_url = base_url

        username = username if username else raw_input("Username: ")
        password = getpass.getpass()
        self.cookies = self._authenticate(username, password)

    def _authenticate(self, username, password):
        """Login with `username` and `password`"""
        r = requests.post(
            self.base_url + "/api/auth/login",
            data=json.dumps({
                "name": username,
                "password": password
            })
        )
        logging.info("{}\n{}".format(r, r.json()))
        return r.cookies
