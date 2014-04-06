from tornado.options import define, options


_CONFIG_FILENAME = "cutthroat.conf"


def define_options():
    """Define defaults for most custom options"""
    # Log file and config file paths
    # Since we are now using supervisord, we just let it capture the
    #   log from STDERR. The following line is therefore commented out.
    # options.log_file_prefix = "/var/log/cutthroat/cutthroat.log"
    define(
        "conf_file_path",
        default="/etc/cutthroat/{}".format(_CONFIG_FILENAME),
        help="Path for the JSON configuration file with customized options",
        type="str"
    )

    # Port
    define(
        "ports",
        default=[8888],
        help=("A list of ports to listen on; each port will be tried"
              " until one can be successfully bound to."),
        type=list
    )

    # Database options
    define(
        "sqlite_db",
        default="/var/lib/cutthroat/cutthroat.db"
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

    define(
        "dblock_file",
        default="/var/lock/cutthroat.tmp",
        type=str,
        help="Location of the lock file used for synchronized DB access."
    )
