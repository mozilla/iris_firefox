import os
import logging
import logging.config

def getLogger(name):
    LOGGING_CONF=os.path.join(os.path.dirname(__file__),"logging.ini")
    logging.config.fileConfig(LOGGING_CONF, disable_existing_loggers=False)
    return logging.getLogger(name)
