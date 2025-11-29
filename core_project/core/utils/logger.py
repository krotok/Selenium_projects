import logging
import logging.config
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any


class LoggerConfig:
    """Centralized logging configuration for core framework"""

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
                'filename': 'logs/automation.log',
                'maxBytes': 10485760,
                'backupCount': 5,
                'encoding': 'utf8'
            }
        },
        'loggers': {
            '': {
                'level': 'DEBUG',
                'handlers': ['console', 'file'],
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

    @classmethod
    def _update_log_levels(cls, config: Dict[str, Any], log_level: str):
        """Update log levels in configuration"""
        if '' in config['loggers']:
            config['loggers']['']['level'] = log_level

        if 'console' in config['handlers']:
            config['handlers']['console']['level'] = log_level

    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """Get logger with given name"""
        return logging.getLogger(name)


# Initialize logging when module is imported
LoggerConfig.setup_logging()