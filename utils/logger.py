import logging
import sys
from datetime import datetime
import os
from typing import Optional


class Logger:
    """Simple logging utility for human-readable logs."""
    
    _instance: Optional['Logger'] = None
    _logger: Optional[logging.Logger] = None
    
    def __new__(cls) -> 'Logger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Set up simple, human-readable logging."""
        self._logger = logging.getLogger('insightful')
        self._logger.setLevel(logging.INFO)  # Only show important stuff
        
        if self._logger.handlers:
            return
        
        # Simple format for humans
        human_formatter = logging.Formatter('%(asctime)s | %(message)s', datefmt='%H:%M:%S')
        
        # Console handler - show key information only
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(human_formatter)
        self._logger.addHandler(console_handler)
        
        # File handler - slightly more detail but still readable
        os.makedirs('logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = f'logs/insightful_{timestamp}.log'
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(human_formatter)
        self._logger.addHandler(file_handler)
        
        # Quiet down noisy libraries
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        logging.getLogger('selenium').setLevel(logging.WARNING)
        logging.getLogger('requests').setLevel(logging.WARNING)
        logging.getLogger('pywinauto').setLevel(logging.WARNING)
    
    @property
    def logger(self) -> logging.Logger:
        """Get the configured logger instance."""
        return self._logger
    
    def info(self, message: str):
        """Log info message."""
        self._logger.info(message)
    
    def debug(self, message: str):
        """Log debug message (won't show in simplified logs)."""
        # Debug messages are hidden in simplified logging
        pass
    
    def warning(self, message: str):
        """Log warning message."""
        self._logger.warning(f"Warning: {message}")
    
    def error(self, message: str):
        """Log error message."""
        self._logger.error(f"Error: {message}")
    
    def exception(self, message: str):
        """Log exception with traceback."""
        self._logger.exception(f"Exception: {message}")
    
    def step(self, description: str):
        """Log a test step clearly."""
        self._logger.info(f"Starting: {description}")
    
    def result(self, description: str, value: str):
        """Log a result clearly."""
        self._logger.info(f"{description}: {value}")
    
    def conversion(self, amount: str, from_curr: str, to_curr: str, result: str, rate: str):
        """Log a currency conversion in simple format."""
        self._logger.info(f"   {amount} {from_curr} → {result} {to_curr} (rate: {rate})")
    
    def test_start(self, test_name: str):
        """Log test start."""
        self._logger.info(f"\nStarting {test_name}")
        self._logger.info("=" * 60)
    
    def test_end(self, test_name: str, status: str):
        """Log test completion."""
        self._logger.info(f"{test_name}: {status}")
        self._logger.info("=" * 60)


logger = Logger()

def get_logger() -> Logger:
    """Get the global logger instance."""
    return logger

def log_info(message: str):
    """Log info message using global logger."""
    logger.info(message)

def log_debug(message: str):
    """Log debug message using global logger."""
    logger.debug(message)

def log_warning(message: str):
    """Log warning message using global logger."""
    logger.warning(message)

def log_error(message: str):
    """Log error message using global logger."""
    logger.error(message)

def log_exception(message: str):
    """Log exception with traceback using global logger."""
    logger.exception(message)

def log_step(description: str):
    """Log a test step clearly."""
    logger.step(description)

def log_result(description: str, value: str):
    """Log a result clearly."""
    logger.result(description, value)

def log_conversion(amount: str, from_curr: str, to_curr: str, result: str, rate: str):
    """Log a currency conversion in simple format."""
    logger.conversion(amount, from_curr, to_curr, result, rate)

def log_test_start(test_name: str):
    """Log test start."""
    logger.test_start(test_name)

def log_test_end(test_name: str, status: str):
    """Log test completion."""
    logger.test_end(test_name, status) 