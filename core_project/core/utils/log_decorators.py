import functools
import time
from typing import Any, Callable
from core_project.core.utils.logger import LoggerConfig


def log_function_call(log_args: bool = True, log_result: bool = False, log_time: bool = True):
    """
    Decorator for automatic function call logging
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = LoggerConfig.get_logger(func.__module__)

            # Log function call
            func_name = func.__name__
            class_name = args[0].__class__.__name__ if args and hasattr(args[0], '__class__') else None

            if class_name:
                log_message = f"{class_name}.{func_name}"
            else:
                log_message = func_name

            if log_args and (args or kwargs):
                args_repr = [repr(a) for a in args[1:]]  # Skip self
                kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
                all_args = ", ".join(args_repr + kwargs_repr)
                log_message += f" with args: {all_args}"

            logger.debug(f"Calling {log_message}")

            # Measure execution time
            start_time = time.time()

            try:
                result = func(*args, **kwargs)

                # Log execution time
                if log_time:
                    execution_time = time.time() - start_time
                    logger.debug(f"{log_message} executed in {execution_time:.3f}s")

                # Log result
                if log_result and result is not None:
                    logger.debug(f"{log_message} returned: {result}")

                return result

            except Exception as e:
                logger.error(f"Error in {log_message}: {str(e)}", exc_info=True)
                raise

        return wrapper

    return decorator


def log_page_interaction(description: str = None):
    """
    Decorator for logging page interactions
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = LoggerConfig.get_logger(func.__module__)

            func_name = func.__name__
            class_name = args[0].__class__.__name__ if args else "Unknown"

            interaction_desc = description or f"{class_name}.{func_name}"
            logger.info(f"Page interaction: {interaction_desc}")

            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Page interaction failed: {interaction_desc} - {str(e)}")
                raise

        return wrapper

    return decorator


class LoggingMixin:
    """Mixin class to provide logging capability to any class"""

    @property
    def logger(self):
        """Get logger for the class"""
        return LoggerConfig.get_logger(self.__class__.__module__)