import logging
from functools import wraps
from django.db import connection
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('student_app')

# define customer decorator for logging the function invoked
def log_invocation(func):
    @wraps(func) # ensure that the function metadata is preserved
    def wrapper(*args, **kwargs):
        logger.debug(f"Function : '{func.__name__}' invoked")
        return func(*args, **kwargs)
    return wrapper


# define custom decorator for logging the http request
def log_http_request(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            logger.debug(f"HTTP Request {request.method} request to {request.path}")
            response= func(request, *args, **kwargs)
            logger.debug(f"HTTP Response: {response.status_code}")
            return response
        except Exception as e:
            logger.exception(f"!!!!An error occcured while processing request to {request.method} sent to {request.path}!!!")
            logger.debug("Exception Details captured in Error Log")
            logger.error(f"Exception details: {e}")
            logger.error("Traceback:")
            logger.error(traceback.format_exc())
            raise # Re-raise the exception to propagate it.
    return wrapper

