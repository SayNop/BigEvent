# from flask_sqlalchemy import SQLAlchemy
#
#
# db = SQLAlchemy()

from .db_routing.routing_sqlalchemy import RoutingSQLAlchemy


db = RoutingSQLAlchemy()
