import os
from dotenv import load_dotenv


load_dotenv()


class BaseConfiguration:
  # Application
  DEBUG = False
  APP_NAME = os.getenv('APP_NAME', 'App Name')
  APP_VER = os.getenv('APP_VER', 'x.y.z')
  APP_DIR = os.path.abspath(os.path.dirname(__file__))
  ROOT_DIR = os.path.abspath(os.path.join(APP_DIR, os.pardir))
  # Static assets
  STATIC_DIR_PATH = os.path.join(APP_DIR, os.getenv('STATIC_DIR_PATH', 'static'))
  USER_AVATAR_DIR = os.path.join(STATIC_DIR_PATH, 'img', "user-avatar")
  _app_dir = APP_DIR[:-1] if APP_DIR[-1] == '/' else APP_DIR  # Strip trailing slash
  _static_dir = STATIC_DIR_PATH[1:] if STATIC_DIR_PATH[0] == '/' else STATIC_DIR_PATH  # Strip trailing slash
  _static_dir = _static_dir[:-1] if _static_dir[-1] == '/' else _static_dir  # Strip starting slash
  USER_AVATAR_DIR = _app_dir + "/" + _static_dir + '/img/user-avatar'
  # Session
  SECRET_KEY = os.getenv('SECRET_KEY', '32_bit_long_random_secret_string')
  SESSION_COOKIE_HTTPONLY = True
  REMEMBER_COOKIE_HTTPONLY = True
  # SQLAlchemy
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLITE_DB_NAME = os.getenv('SQLITE_DB_NAME', 'db.sqlite3')
  SQLITE_PATH = 'sqlite:///' + os.path.join(ROOT_DIR, SQLITE_DB_NAME)
  SQLALCHEMY_DATABASE_URI = SQLITE_PATH
  # Content-Encoding/Compression
  COMPRESS_ALGORITHM = 'gzip'
  COMPRESS_REGISTER = True
  # Local Timezome
  LOCAL_TIMEZONE = os.getenv('LOCAL_TIMEZONE', 'Asia/Dhaka')
  # Bootstrap
  BOOTSTRAP_SERVE_LOCAL = True
  # BOOTSTRAP_BOOTSWATCH_THEME='cerulean'


class DevelopmentConfiguration(BaseConfiguration):
  # Application
  DEBUG = True
  APP_NAME = '~{0}'.format(BaseConfiguration.APP_NAME)
  # Template debugging
  TEMPLATES_AUTO_RELOAD = True
  EXPLAIN_TEMPLATE_LOADING = False
  # Session
  SESSION_COOKIE_HTTPONLY = False
  REMEMBER_COOKIE_HTTPONLY = False
  REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 1  # 1 days
  # SQLAlchemy
  SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfiguration(BaseConfiguration):
  DEBUG = False
  # Session
  REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7 days
  # MySql
  # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(os.getenv('DB_ENGINE', 'mysql'),
  #                                                        os.getenv('DB_USERNAME', 'mysql_db_user'),
  #                                                        os.getenv('DB_PASSWORD', 'mysql_db_user'),
  #                                                        os.getenv('DB_HOST', 'mysql_db_host'),
  #                                                        os.getenv('DB_PORT', 3306),
  #                                                        os.getenv('DB_NAME', 'mysql_db_name'))
