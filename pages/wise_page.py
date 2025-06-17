from typing import Dict, List
import time
from .base_page import BasePage
from utils.logger import log_info, log_debug


class WisePage(BasePage):
    """Wise.com page object."""
    
    URL = "https://wise.com/gb/currency-converter/"
    
    # Currency Selection Locators
    FROM_CURRENCY_BUTTON = "#source-inputSelectedCurrency"
    FROM_CURRENCY_SEARCH = "#source-inputSelectedCurrencySearch"
    TO_CURRENCY_BUTTON = "#target-inputSelectedCurrency"
    TO_CURRENCY_SEARCH = "#target-inputSelectedCurrencySearch"
    
    # Dropdown Options (XPath)
    DROPDOWN_RSD = "//section[contains(@class, 'np-select-input-listbox-container')]//div[contains(@class, 'd-inline') and contains (text(), 'RSD')]"
    DROPDOWN_EUR = "//section[contains(@class, 'np-select-input-listbox-container')]//div[contains(@class, 'd-inline') and contains (text(), 'EUR')]"
    DROPDOWN_USD = "//section[contains(@class, 'np-select-input-listbox-container')]//div[contains(@class, 'd-inline') and contains (text(), 'USD')]"
    
    # Amount Input/Output Locators
    AMOUNT_INPUT = "#source-input"
    RESULT_INPUT = "#target-input"

    def get_rsd_conversions(self, amounts: List[float]) -> List[Dict]:
        """Get RSD to EUR and USD conversions with static sleeps."""
        log_info("  Starting Wise.com browser operations...")
        results = []
        
        # Navigate to Wise.com
        log_debug(f"  Navigating to: {self.URL}")
        self.navigate_to(self.URL)
        log_info("  Successfully loaded Wise.com currency converter")
        
        # Select RSD for FROM currency
        log_debug("  Setting up FROM currency (RSD)...")
        from_currency_button = self.page.locator(self.FROM_CURRENCY_BUTTON)
        from_currency_button.click()
        log_debug("  FROM currency dropdown opened")
        from_currency_button_search = self.page.locator(self.FROM_CURRENCY_SEARCH)
        from_currency_button_search.fill("RSD")
        log_debug("  Typed 'RSD' in FROM currency search")
        dd_rsd = self.page.locator(self.DROPDOWN_RSD)
        dd_rsd.click()
        log_info("  FROM currency set to RSD")

        
        # RSD → EUR conversions (ascending order: 1000, 2000, 3000)
        log_debug("  Setting up TO currency (EUR)...")
        to_currency_button = self.page.locator(self.TO_CURRENCY_BUTTON)
        to_currency_button.click()
        log_debug("  TO currency dropdown opened")
        to_currency_button_search = self.page.locator(self.TO_CURRENCY_SEARCH)
        to_currency_button_search.fill("EUR")
        log_debug("  Typed 'EUR' in TO currency search")
        dd_eur = self.page.locator(self.DROPDOWN_EUR)
        dd_eur.click()
        log_info("  TO currency set to EUR")

        
        log_info("  Starting RSD → EUR conversions...")
        for i, amount in enumerate(amounts, 1):
            log_debug(f"    Processing EUR conversion {i}/3: {amount} RSD")
            amount_input = self.page.locator(self.AMOUNT_INPUT)
            amount_input.wait_for(state="visible")
            amount_input.clear()
            amount_input.fill(str(amount))
            log_debug(f"    Amount {amount} entered")
            
            # Static wait for conversion
            time.sleep(0.5)
            log_debug("    Waiting for conversion to complete...")
            
            # Extract data and create result
            converted_amount, rate = self._extract_data(amount)
            result = self.create_result(amount, "RSD", "EUR", converted_amount, rate, "Wise.com")
            results.append(result)
            log_debug(f"    WISE EXTRACTION - Amount: {amount} RSD")
            log_debug(f"    WISE EXTRACTION - Converted: {converted_amount:.8f} EUR")
            log_debug(f"    WISE EXTRACTION - Rate: {rate:.10f} (full precision)")
            log_debug(f"    Result: {amount} RSD = {converted_amount:.4f} EUR (rate: {rate:.8f})")
        log_info("  RSD → EUR conversions completed")
        
        # RSD → USD conversions (ascending order: 1000, 2000, 3000)
        log_debug("  Switching TO currency to USD...")
        to_currency_button.click()
        to_currency_button_search.fill("USD")
        log_debug("  Typed 'USD' in TO currency search")
        dd_usd = self.page.locator(self.DROPDOWN_USD)
        dd_usd.click()
        log_info("  TO currency changed to USD")
        
        log_info("  Starting RSD → USD conversions...")
        for i, amount in enumerate(amounts, 1):
            log_debug(f"    Processing USD conversion {i}/3: {amount} RSD")
            amount_input = self.page.locator(self.AMOUNT_INPUT)
            amount_input.clear()
            amount_input.fill(str(amount))
            log_debug(f"    Amount {amount} entered")
            
            # Static wait for conversion
            time.sleep(1)
            log_debug("    Waiting for conversion to complete...")
            
            # Extract data and create result
            converted_amount, rate = self._extract_data(amount)
            result = self.create_result(amount, "RSD", "USD", converted_amount, rate, "Wise.com")
            results.append(result)
            log_debug(f"    WISE EXTRACTION - Amount: {amount} RSD")
            log_debug(f"    WISE EXTRACTION - Converted: {converted_amount:.8f} USD")
            log_debug(f"    WISE EXTRACTION - Rate: {rate:.10f} (full precision)")
            log_debug(f"    Result: {amount} RSD = {converted_amount:.4f} USD (rate: {rate:.8f})")
        log_info("  RSD → USD conversions completed")
        
        log_info(f"  Wise.com browser operations completed - {len(results)} conversions collected")
        return results
    
    def _extract_data(self, original_amount: float) -> tuple:
        """Extract converted amount and exchange rate."""
        converted_amount = 0.0
        
        # Get converted amount from target input
        try:
            target_value = self.page.locator(self.RESULT_INPUT).input_value() or ""
            converted_amount = self.extract_number_from_text(target_value)
            log_debug(f"      Extracted converted amount: {converted_amount}")
        except Exception as e:
            log_debug(f"      Failed to extract converted amount: {e}")
        
        # Calculate exchange rate using base class method
        exchange_rate = self.calculate_exchange_rate(converted_amount, original_amount)
        log_debug(f"      Calculated exchange rate: {exchange_rate}")
        
        return converted_amount, exchange_rate 