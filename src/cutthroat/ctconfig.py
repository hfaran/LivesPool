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
