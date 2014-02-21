from tornado_json.routes import get_routes

from cutthroat import api
from cutthroat import views


def assemble_routes():
    """Assembles all routes and returns"""
    custom_routes = [("/", views.signin.Landing)]
    api_routes = get_routes(api)
    view_routes = map(
        lambda r: (r[0].replace("/views", "", 1), r[1]),
        get_routes(views)  # View routes with /views removed
    )
    return api_routes + view_routes + custom_routes
