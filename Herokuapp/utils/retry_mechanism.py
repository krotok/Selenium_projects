import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

logger = logging.getLogger(__name__)


def retry_on_exception(
        max_attempts: int = 3,
        delay: float = 1.0,
        exceptions: tuple = (Exception,),
        backoff_factor: float = 2.0
):
    """
    Retry decorator for functions that might fail temporarily

    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        exceptions: Tuple of exceptions to catch and retry on
        backoff_factor: Multiplier for delay after each attempt
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_attempts - 1:
                        logger.error(f"Function {func.__name__} failed after {max_attempts} attempts")
                        raise

                    logger.warning(
                        f"Attempt {attempt + 1}/{max_attempts} failed for {func.__name__}: {e}. "
                        f"Retrying in {current_delay} seconds..."
                    )
                    time.sleep(current_delay)
                    current_delay *= backoff_factor

            raise last_exception

        return wrapper

    return decorator


class RetryMechanism:
    def __init__(self, max_attempts: int = 3, delay: float = 1.0):
        self.max_attempts = max_attempts
        self.delay = delay

    def execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with retry logic"""
        last_exception = None

        for attempt in range(self.max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt == self.max_attempts - 1:
                    raise last_exception

                logger.warning(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(self.delay)

        raise last_exception