import logging.config

logging.config.fileConfig('./config/logging.conf')
logger = logging.getLogger("simpleExample")