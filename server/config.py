import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
	try:
		SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
	except:
		SECRET_KEY = os.environment.get('SECRET_KEY') or 'hard to guess string'
	try:
		MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.163.com')
	except:
		MAIL_SERVER = os.environment.get('MAIL_SERVER', 'smtp.163.com')
	try:
		MAIL_PORT = os.environ.get('MAIL_PORT', '25')
	except:
		MAIL_PORT = os.environment.get('MAIL_PORT', '25')
	try:
		MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	except:
		MAIL_USERNAME = os.environment.get('MAIL_USERNAME')
	try:
		MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	except:
		MAIL_PASSWORD = os.environment.get('MAIL_PASSWORD')
	try:
		FLASKY_MAIL_SENDER = os.environ.get('FLASKY_ADMIN')
	except:
		FLASKY_MAIL_SENDER = os.environment.get('FLASKY_ADMIN')
	try:
		FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	except:
		FLASKY_ADMIN = os.environment.get('FLASKY_ADMIN')
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	try:
		SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
	except:
		SQLALCHEMY_DATABASE_URI = os.environment.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	try:
		SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
			'sqlite://'
	except:
		SQLALCHEMY_DATABASE_URI = os.environment.get('TEST_DATABASE_URL') or \
			'sqlite://'


class ProductionConfig(Config):
	try:
		SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
			'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	except:
		SQLALCHEMY_DATABASE_URI = os.environment.get('DATABASE_URL') or \
			'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
	}
