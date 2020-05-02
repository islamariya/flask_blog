import secrets


class Configuration(object):
    SECRET_KEY = secrets.token_urlsafe(16)
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog_db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


POSTS_PER_PAGE = 3