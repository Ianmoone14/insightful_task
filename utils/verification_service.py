from typing import Dict
from utils.logger import log_info, log_debug


class VerificationService:
    """Simple service to verify web scraping results match calculator results."""
    
    def __init__(self, tolerance: float = 0.01):
        self.tolerance = tolerance  # Allow 1 cent difference for floating point precision
    
    def assert_conversions_match(self, web_data: Dict, calculator_data: Dict, source: str) -> bool:
        """
        Assert that web scraping results match calculator results.
        
        Args:
            web_data: Web scraping results from XE/Wise
            calculator_data: Calculator computation results using same exchange rates
            source: Source name (e.g., 'XE.com', 'Wise.com')
            
        Returns:
            True if all conversions match within tolerance
            
        Raises:
            AssertionError: If conversions don't match
        """
        log_info(f"Verifying {source} - Web vs Calculator conversion accuracy...")
        
        # Check EUR conversions
        eur_matches = self._verify_currency_conversions(
            web_data["eur"], calculator_data["eur"], "EUR", source
        )
        
        # Check USD conversions  
        usd_matches = self._verify_currency_conversions(
            web_data["usd"], calculator_data["usd"], "USD", source
        )
        
        # Overall assertion
        if eur_matches and usd_matches:
            log_info(f" {source} verification PASSED - All conversions match within tolerance")
            return True
        else:
            raise AssertionError(f" {source} verification FAILED - Conversions don't match")
    
    def _verify_currency_conversions(self, web_currency_data: Dict, calc_currency_data: Dict, 
                                   currency: str, source: str) -> bool:
        """Verify conversions for a specific currency (EUR or USD)."""
        log_debug(f"Checking {currency} conversions for {source}...")
        
        web_conversions = web_currency_data["conversions"]
        calc_conversions = calc_currency_data["conversions"]
        web_rate = web_currency_data["exchange_rate"]
        calc_rate = calc_currency_data["exchange_rate"]
        
        # Exchange rates should be exactly the same (calculator uses web rate)
        if abs(web_rate - calc_rate) > 0.00000001:
            log_debug(f" {currency} exchange rates don't match: Web={web_rate:.8f}, Calc={calc_rate:.8f}")
            return False
        
        # Check each conversion
        all_match = True
        for amount in web_conversions:
            if amount in calc_conversions:
                web_result = web_conversions[amount]
                calc_result = calc_conversions[amount]
                difference = abs(web_result - calc_result)
                
                if difference > self.tolerance:
                    log_info(f"❌ {amount} RSD → {currency}: Web={web_result:.4f}, Calc={calc_result:.4f}, "
                             f"Diff={difference:.4f} (exceeds tolerance {self.tolerance})")
                    all_match = False
                else:
                    log_debug(f"✓ {amount} RSD → {currency}: Web={web_result:.4f}, Calc={calc_result:.4f}, "
                             f"Diff={difference:.4f} (within tolerance {self.tolerance})")
        
        return all_match 