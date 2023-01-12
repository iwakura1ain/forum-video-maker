import logging
from functools import wraps

logger = None

def startLogger():
    global logger
    if logger is None:
        logging.basicConfig(filename="test.log", level=logging.INFO)
        logger = logging.getLogger("test")

def setLogger(passed_logger):
    global logger
    logger = passed_logger
        
def logCall(logStr):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(logStr)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def logInfo(logStr):
    logger.info(logStr)

    
def logError(logStr):
    logger.error(logStr)
