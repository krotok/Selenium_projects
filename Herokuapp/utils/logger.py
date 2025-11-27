import logging
import logging.config
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class LoggerConfig:
    """Centralized logging configuration for Herokuapp project"""

    DEFAULT_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'json': {
                'format': '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "file": "%(filename)s", "line": "%(lineno)d", "function": "%(funcName)s", "message": "%(message)s"}',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'filename': 'logs/herokuapp_automation.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'error_file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'detailed',
                'filename': 'logs/herokuapp_errors.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf8'
            },
            'allure_handler': {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout'
            }
        },
        'loggers': {
            '': {  # root logger
                'level': 'DEBUG',
                'handlers': ['console', 'file', 'error_file'],
                'propagate': False
            },
            'selenium': {
                'level': 'WARNING',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'urllib3': {
                'level': 'WARNING',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'pages': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'services': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'tests': {
                'level': 'DEBUG',
                'handlers': ['console', 'file', 'error_file', 'allure_handler'],
                'propagate': False
            },
            'utils': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            },
            'wiremock': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }

    @classmethod
    def setup_logging(cls, config: Optional[Dict[str, Any]] = None, log_level: str = 'INFO'):
        """Setup centralized logging configuration"""

        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)

        # Use provided config or default
        logging_config = config or cls.DEFAULT_CONFIG

        # Update log levels based on parameter
        if log_level:
            cls._update_log_levels(logging_config, log_level)

        # Apply configuration
        logging.config.dictConfig(logging_config)

        # Capture warnings
        logging.captureWarnings(True)

        logger = logging.getLogger(__name__)
        logger.info("Herokuapp logging configuration initialized")

    @classmethod
    def _update_log_levels(cls, config: Dict[str, Any], log_level: str):
        """Update log levels in configuration"""
        # Update root logger
        if '' in config['loggers']:
            config['loggers']['']['level'] = log_level

        # Update console handler
        if 'console' in config['handlers']:
            config['handlers']['console']['level'] = log_level

        # Update specific loggers
        for logger_name in ['pages', 'services', 'tests', 'utils', 'wiremock']:
            if logger_name in config['loggers']:
                config['loggers'][logger_name]['level'] = log_level

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get logger with given name"""
        return logging.getLogger(name)


# Initialize logging when module is imported
LoggerConfig.setup_logging()