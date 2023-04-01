import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # the database pagination
    FLASKY_POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1a2b3c4d@localhost:3306/teachingplatform'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://eyes_user:+Yw{j0tw%YJd4(m@qingvoice.mysql.rds.aliyuncs.com:3306/eyes'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://eyes_user:+Yw{j0tw%YJd4(m@qingvoice.mysql.rds.aliyuncs.com:3306/eyes'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
