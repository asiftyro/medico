import logging
from logging.config import dictConfig
from application.configuration import BaseConfiguration

dictConfig(BaseConfiguration.LOG_SCHEMA)
logger = logging.getLogger(__name__)
