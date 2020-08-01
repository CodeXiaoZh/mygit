import os

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15

    DEBUG = True

class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:852000@127.0.0.1/yunlog'

config = {
    'development': DevelopmentConfig
}