import logging
import time
import os
from functools import wraps
from flask import g, jsonify, request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_file = os.path.join(os.getcwd(), "logfile.log")
file_handler = logging.FileHandler(filename=log_file)
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(levelname)s - %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def log_execution(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.debug(f"Starting execution of {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(
                f"Completed {func.__name__} in {time.time() - start_time:.2f} seconds"
            )
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    return wrapper

def login_required_to_api(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if request.method == "OPTIONS":
            response = jsonify({"message": "Preflight request allowed"})
            response.status_code = 204  # No Content
            return response

        if g.user is None:
            return jsonify({"error": "Unauthorized"}), 401
        return view(**kwargs)
    return wrapped_view
