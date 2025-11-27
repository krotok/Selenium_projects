from .logger import LoggerConfig
from .log_decorators import log_function_call, log_page_interaction, LoggingMixin
from .custom_waits import CustomWaits
from .retry_mechanism import retry_on_exception, RetryMechanism

# Export the main functions
setup_logging = LoggerConfig.setup_logging
get_logger = LoggerConfig.get_logger

__all__ = [
    'LoggerConfig',
    'setup_logging',
    'get_logger',
    'log_function_call',
    'log_page_interaction',
    'LoggingMixin',
    'CustomWaits',
    'retry_on_exception',
    'RetryMechanism'
]