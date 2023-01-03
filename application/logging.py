import logging
from dotenv import load_dotenv
import os
from logging.config import dictConfig
from application.configuration import BaseConfiguration

load_dotenv()

enable_logger = int(os.getenv("ENABLE_LOGGER_CONFIG", '1').strip())
if enable_logger:
    dictConfig(BaseConfiguration.LOG_SCHEMA)
logger = logging.getLogger(__name__)

