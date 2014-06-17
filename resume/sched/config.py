"""Application configuration.

When using app.config.from_object(obj), Flask will look for all UPPERCASE
attributes on that object and load their values into the app config. Python
modules are objects, so you can use a .py file as your configuration.
"""

import os

# Get the current working directory to place sched.db during development.
# In production, use absolute paths or a database management system.

class BaseConfig(object):
    PWD = os.path.abspath(os.curdir)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/sched.db'.format(PWD)
    #SQLALCHEMY_DATABASE_URI = 'sqlite:////home/ziliot/webapps/appname3/sched.db'
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ziliot:ziliot01@web437.webfaction.com:5432/internly";


class DefaultConfig(BaseConfig):
    SECRET_KEY = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf' # Create your own.
    SESSION_PROTECTION = 'strong'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    SECURITY_PASSWORD_SALT = 'enydM2ANhdcoKwdVa0jWvEsbPFuQpMjf'
    SECURITY_LOGIN_URL = '/login'
    SECURITY_LOGOUT_URL = '/logout'
    SECURITY_REGISTER_URL = '/signup'
    SECURITY_RESET_URL = '/reset'
    SECURITY_CONFIRMABLE = False
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False
    FACEBOOK_LOGIN_APP_ID = '249060078624564'
    FACEBOOK_LOGIN_APP_SECRET = 'c2ef65f4d7ffed2549f6b0c0646f4a86'
    LINKEDIN_LOGIN_API_KEY = '75xxogitps4187w'
    LINKEDIN_LOGIN_SECRET_KEY = '2U091SyHRol7z0Mk'

