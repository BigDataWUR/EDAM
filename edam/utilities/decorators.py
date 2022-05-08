import functools
import time

from edam import get_logger

logger = get_logger(__name__)


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - start_time
        logger.debug(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value

    return wrapper_timer
