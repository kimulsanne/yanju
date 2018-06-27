import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

SECRET_KEY = 'my_precious'
'''DEBUG = False
SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
DEBUG_TB_ENABLED = False
STRIPE_SECRET_KEY = 'foo'
STRIPE_PUBLISHABLE_KEY = 'bar'''''
SECURITY_PASSWORD_SALT = 'my_precious_two'

1111
