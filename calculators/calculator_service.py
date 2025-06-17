from typing import Dict, List
from utils.logger import log_info, log_debug, log_error
from utils.os_utils import detect_os, get_calculator_class
from .base_calculator import BaseCalculator


class CalculatorService:
    """
    Cross-platform calculator service that automatically detects the operating system
    and uses the appropriate calculator implementation.
    """
    
    def __init__(self):
        self._calculator = None
        self._initialize_calculator()
    
    def _initialize_calculator(self):
        """Initialize the appropriate calculator based on the operating system."""
        calculator_class = get_calculator_class()
        self._calculator = calculator_class()
        log_info(f"Calculator service initialized for {self._calculator.get_platform_name()}")
    
    def calculate_conversions(self, amounts: List[float], exchange_rates: Dict, source: str) -> Dict:
        """
        Calculate currency conversions using the platform's native calculator.
        
        Args:
            amounts: List of amounts to convert (e.g., [1000, 2000, 3000])
            exchange_rates: Dict with 'eur' and 'usd' rates (e.g., {'eur': 0.00853, 'usd': 0.00988})
            source: Source of the exchange rates (e.g., 'XE.com')
            
        Returns:
            Dict with structured conversion results including calculated values
        """
        if not self._calculator:
            raise RuntimeError("Calculator service not properly initialized")
        
        log_debug(f"Starting calculator conversions for {source} using {self._calculator.get_platform_name()}")
        return self._calculator.calculate_conversions(amounts, exchange_rates, source)
    
    def get_calculator_info(self) -> Dict[str, str]:
        """
        Get information about the current calculator implementation.
        
        Returns:
            Dict containing platform name and implementation details
        """
        if not self._calculator:
            return {"platform": "unknown", "status": "not initialized"}
        
        return {
            "platform": self._calculator.get_platform_name(),
            "status": "initialized",
            "implementation": self._calculator.__class__.__name__
        }
    
    @staticmethod
    def get_supported_platforms() -> List[str]:
        """
        Get list of supported platforms.
        
        Returns:
            List of supported platform names
        """
        return ["Windows", "Linux"]
    
    @staticmethod
    def is_platform_supported(platform_name: str = None) -> bool:
        """
        Check if the current or specified platform is supported.
        
        Args:
            platform_name: Optional platform name to check. If None, checks current platform.
            
        Returns:
            True if platform is supported, False otherwise
        """
        if platform_name is None:
            platform_name = detect_os()
        
        return platform_name.lower() in ["windows", "linux"] 