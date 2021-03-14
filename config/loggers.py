import logging


def log_exception(msg=None):
    """
    Called explicitly to log exceptions
    """
    logger = logging.getLogger("exception")
    logger.exception(msg=msg)
