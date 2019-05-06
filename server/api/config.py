# imports some base configurations
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
	DEBUG = True
	BCRYPT_LOG_ROUNDS = 13
	SQLALCHEMY_TRACK_MODIFICATIONS = False
