import logging
import json
from tornado.options import define, options


_CONFIG_FILENAME = "cutthroat.conf"


def define_options():
    """Define defaults for most custom options"""
    # Log file and config file paths
    options.log_file_prefix = "/var/log/cutthroat/cutthroat.log"
    define(
        "conf_file_path",
        default="/etc/cutthroat/{}".format(_CONFIG_FILENAME),
        help="Path for the JSON configuration file with customized options",
        type="str"
    )

    # Port
    define(
        "port",
        default=8888,
        help="run on the given port",
        type=int
    )

    # Database options
    define(
        "sqlite_db",
        default="cutthroat.db"
    )

    define(
        "output_routes",
        default=True,
        type=bool,
        help="If enabled, outputs all application routes to `routes.json`"
    )

    define(
        "session_timeout_days",
        default=1,
        help=("Cookie expiration time in days; can also be set to `None` "
              "for session cookies, i.e., cookies that expire when "
              "browser window is closed.")
    )

    define(
        "cookie_secret",
        default="",
        type=str,
        help=("Set this to an empty string to generate a new cookie secret "
              "each time the server is restarted, or to any string which is "
              "the cookie secret.")
    )
