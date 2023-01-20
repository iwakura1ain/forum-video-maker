import logging
from functools import wraps

logger = None

def startLogger(filename="test.log", level=logging.INFO, mode="w"):
    global logger
    if logger is None:
        logging.basicConfig(filename=filename, level=level, filemode=mode)
        logger = logging.getLogger("forum-video-maker")

def setLogger(passed_logger):
    global logger
    logger = passed_logger
        
def logCall(logStr):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(logStr)
            print(logStr)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def logInfo(logStr):
    print(logStr)
    logger.info(logStr)


def logDebug(logStr):
    print(logStr)
    logger.debug(logStr)
    
    
def logError(logStr):
    print(logStr)
    logger.error(logStr)
