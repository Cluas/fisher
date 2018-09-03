import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '*^xz&yxh&22)(%57zt%3y1-fd$5+a58n#rc%=gzc4f6$mp%qc-'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    BOOK_PRE_PAGE = 15
    BEANS_UPLOAD_ONE_BOOK = 0.5
    RECENT_BOOK_COUNT = 20
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_SUE_TSL = False
    MAIL_USERNAME = 'admin@cluas.me'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or '*****'
    MAIL_SUBJECT_PREFIX = '【鱼书】'
    MAIL_SENDER = '鱼书 Admin <admin@cluas.me>'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DEV_DATABASE_URL')
                               or
                               'mysql+cymysql://root:imyuols123@localhost:3306/fisher_dev')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (os.environ.get('TEST_DATABASE_URL')
                               or
                               'mysql+cymysql://root:imyuols123@localhost:3306/fisher_test')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = (os.environ.get('DATABASE_URL')
                               or
                               'mysql+cymysql://root:imyuols123@localhost:3306/fisher')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
