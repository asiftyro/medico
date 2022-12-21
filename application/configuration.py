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
  STATIC_DIR_PATH = os.getenv('STATIC_DIR_PATH', 'static')
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


class DevelopmentConfiguration(BaseConfiguration):
  # Application
  DEBUG = True
  APP_NAME = "~{0}".format(BaseConfiguration.APP_NAME)
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
  #Session
  REMEMBER_COOKIE_DURATION = 60 * 60 * 24 * 7  # 7 days
  # MySql
  # SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(os.getenv('DB_ENGINE', 'mysql'),
  #                                                        os.getenv('DB_USERNAME', 'mysql_db_user'),
  #                                                        os.getenv('DB_PASSWORD', 'mysql_db_user'),
  #                                                        os.getenv('DB_HOST', 'mysql_db_host'),
  #                                                        os.getenv('DB_PORT', 3306),
  #                                                        os.getenv('DB_NAME', 'mysql_db_name'))
