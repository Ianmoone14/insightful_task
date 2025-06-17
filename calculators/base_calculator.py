from abc import ABC, abstractmethod
from typing import Dict, List
from utils.logger import log_info, log_debug


class BaseCalculator(ABC):
    """Abstract base class for calculator implementations."""
    
    def __init__(self):
        self.calculator_open = False
    
    @abstractmethod
    def calculate_conversions(self, amounts: List[float], exchange_rates: Dict, source: str) -> Dict:
        """
        Calculate currency conversions using the platform's calculator.
        
        Args:
            amounts: List of amounts to convert (e.g., [1000, 2000, 3000])
            exchange_rates: Dict with 'eur' and 'usd' rates (e.g., {'eur': 0.00853, 'usd': 0.00988})
            source: Source of the exchange rates (e.g., 'XE.com')
            
        Returns:
            Dict with structured conversion results including calculated values
        """
        pass
    
    @abstractmethod
    def _open_calculator(self):
        """Open the platform-specific calculator application."""
        pass
    
    @abstractmethod
    def _close_calculator(self):
        """Close the calculator application."""
        pass
    
    @abstractmethod
    def _perform_calculation(self, amount: float, rate: float) -> float:
        """
        Perform a single multiplication calculation.
        
        Args:
            amount: The amount to multiply
            rate: The exchange rate to multiply by
            
        Returns:
            The calculated result
        """
        pass
    
    def _create_results_structure(self, amounts: List[float], exchange_rates: Dict, source: str) -> Dict:
        """Create the standard results structure."""
        return {
            "source": f"{source} + Calculator",
            "eur": {
                "exchange_rate": exchange_rates["eur"],
                "conversions": {}
            },
            "usd": {
                "exchange_rate": exchange_rates["usd"], 
                "conversions": {}
            }
        }
    
    def _log_calculation_start(self, currency: str, rate: float):
        """Log the start of calculations for a currency."""
        log_info(f"Calculating {currency} conversions using {self.get_platform_name()} Calculator...")
        log_debug(f"Exchange rate: {rate:.8f}")
    
    def _log_calculation_result(self, amount: float, rate: float, result: float, currency: str):
        """Log individual calculation results."""
        log_debug(f"{amount} RSD × {rate:.8f} = {result:.4f} {currency}")
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Return the name of the platform (e.g., 'Windows', 'macOS', 'Ubuntu')."""
        pass 