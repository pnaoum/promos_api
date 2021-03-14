import logging


def log_exception(msg=None):
    logger = logging.getLogger("exception")
    logger.exception(msg=msg)
