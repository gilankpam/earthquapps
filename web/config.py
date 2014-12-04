import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://root:@127.0.0.1/earthquake'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SECRET_KEY = 'jhka89&DS(Yuhdslsh8(O'
DEBUG = True

# Beanstalk config
BEANSTALK = {
    'HOST': "localhost",
    'PORT': 14711
}
