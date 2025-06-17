from typing import Dict, List
import re
import time
from .base_page import BasePage
from utils.logger import log_info, log_debug


class XEPage(BasePage):
    """XE.com page object."""
    
    URL = "https://www.xe.com/"
    
    # Currency Selection Locators
    FROM_CURRENCY_INPUT = "#midmarketFromCurrency input[placeholder='Type to search...']"
    TO_CURRENCY_INPUT = "#midmarketToCurrency input[placeholder='Type to search...']"
    
    # Search Options
    SERBIA_OPTION = "Serbia"
    EUR_OPTION = "EUR Euro"
    USD_OPTION = "US Dollar"
    
    # Action Button
    CONVERT_BUTTON = "button:has-text('Convert')"
    
    # Amount and Result Locators
    AMOUNT_INPUT = "#amount"
    CONVERSION_FIELD = "[data-testid='conversion']"
    RESULT_ELEMENTS = "[data-testid='conversion'] .sc-708e65be-1"
    
    # Dynamic XPath pattern for result validation
    RESULT_XPATH_TEMPLATE = "(//div[@class='[grid-area:conversion]']//p[contains(text(),'{amount}')])[1]"
    
    def get_rsd_conversions(self, amounts: List[float]) -> List[Dict]:
        """Get RSD to EUR and USD conversions with consistent flow."""
        log_info("  Starting XE.com browser operations...")
        results = []
        
        # Navigate to XE.com
        log_debug(f"  Navigating to: {self.URL}")
        self.navigate_to(self.URL)
        log_info("  Successfully loaded XE.com homepage")
        
        # Select Serbia (RSD) for FROM currency
        log_debug("  Setting up FROM currency (Serbia/RSD)...")
        from_input = self.page.locator(self.FROM_CURRENCY_INPUT)
        from_input.click()
        log_debug("  FROM currency input clicked")
        from_input.fill(self.SERBIA_OPTION)
        log_debug(f"  Typed '{self.SERBIA_OPTION}' in FROM currency search")
        self.page.get_by_role("option", name=self.SERBIA_OPTION).click()
        log_info("  FROM currency set to Serbia (RSD)")
        
        # Select EUR for TO currency
        log_debug("  Setting up TO currency (EUR)...")
        to_input = self.page.locator(self.TO_CURRENCY_INPUT)
        to_input.wait_for(state="visible")
        to_input.click()
        log_debug("  TO currency input clicked")
        to_input.fill("Euro")
        log_debug("  Typed 'Euro' in TO currency search")
        self.page.get_by_role("option", name=self.EUR_OPTION).first.click()
        log_info("  TO currency set to EUR")
        
        # Click Convert button once
        log_debug("  Clicking Convert button...")
        convert_button = self.page.locator(self.CONVERT_BUTTON)
        convert_button.wait_for(state="visible")
        convert_button.click()
        log_info("  Convert button clicked, waiting for conversion rate...")
        
        # Wait for conversion rate to appear (confirms page is ready)
        conversion_field = self.page.locator(self.CONVERSION_FIELD).first
        conversion_field.wait_for(state="visible", timeout=10000)
        log_info("  Conversion interface is ready")
        
        # Get amount input
        amount_input = self.page.locator(self.AMOUNT_INPUT)
        
        # RSD → EUR conversions: 1000, 2000, 3000
        log_info("  Starting RSD → EUR conversions...")
        for i, amount in enumerate(amounts, 1):
            log_debug(f"    Processing EUR conversion {i}/3: {amount} RSD")
            amount_input.clear()
            amount_input.fill(str(amount))
            log_debug(f"    Amount {amount} entered")

            conversion_field.click()
            formated_amount = amount_input.get_attribute("value", timeout=500)
            xpath = self.RESULT_XPATH_TEMPLATE.format(amount=formated_amount)
            self.page.locator(xpath).wait_for(state="visible")
            log_debug(f"    Conversion result visible for {amount} RSD")

            # Extract data and create result
            converted_amount, rate = self._extract_data(amount)
            result = self.create_result(amount, "RSD", "EUR", converted_amount, rate, "XE.com")
            results.append(result)
            log_debug(f"    XE EXTRACTION - Amount: {amount} RSD")
            log_debug(f"    XE EXTRACTION - Converted: {converted_amount:.8f} EUR")
            log_debug(f"    XE EXTRACTION - Rate: {rate:.10f} (full precision)")
            log_debug(f"    Result: {amount} RSD = {converted_amount:.4f} EUR (rate: {rate:.8f})")
        log_info("  RSD → EUR conversions completed")

        # Change to USD
        log_debug("  Switching TO currency to USD...")
        to_input.click()
        to_input.fill("USD")
        log_debug("  Typed 'USD' in TO currency search")
        self.page.get_by_role("option", name=self.USD_OPTION).click()
        log_info("  TO currency changed to USD")
        time.sleep(2)  # Short wait for currency change
        
        # Clear amount input and enter test data again: 1000, 2000, 3000
        log_info("  Starting RSD → USD conversions...")
        for i, amount in enumerate(amounts, 1):
            log_debug(f"    Processing USD conversion {i}/3: {amount} RSD")
            amount_input.clear()
            amount_input.fill(str(amount))
            log_debug(f"    Amount {amount} entered")
            
            conversion_field.click()
            formated_amount = amount_input.get_attribute("value", timeout=500)
            xpath = self.RESULT_XPATH_TEMPLATE.format(amount=formated_amount)
            self.page.locator(xpath).wait_for(state="visible")
            log_debug(f"    Conversion result visible for {amount} RSD")
            
            # Extract data and create result
            converted_amount, rate = self._extract_data(amount)
            result = self.create_result(amount, "RSD", "USD", converted_amount, rate, "XE.com")
            results.append(result)
            log_debug(f"    XE EXTRACTION - Amount: {amount} RSD")
            log_debug(f"    XE EXTRACTION - Converted: {converted_amount:.8f} USD")
            log_debug(f"    XE EXTRACTION - Rate: {rate:.10f} (full precision)")
            log_debug(f"    Result: {amount} RSD = {converted_amount:.4f} USD (rate: {rate:.8f})")
        log_info("  RSD → USD conversions completed")
        
        log_info(f"  XE.com browser operations completed - {len(results)} conversions collected")
        return results
    
    def _extract_data(self, original_amount: float) -> tuple:
        """Extract converted amount and exchange rate."""
        converted_amount = 0.0
        exchange_rate = 0.0
        
        # Try to get converted amount
        try:
            result_elements = self.page.locator(self.RESULT_ELEMENTS)
            if result_elements.count() > 0:
                text = result_elements.first.text_content() or ""
                converted_amount = self.extract_number_from_text(text)
                log_debug(f"      Extracted converted amount: {converted_amount}")
        except Exception as e:
            log_debug(f"      Failed to extract converted amount: {e}")
        
        # Try to get exchange rate
        try:
            rate_elements = self.page.locator(self.CONVERSION_FIELD)
            for i in range(rate_elements.count()):
                text = rate_elements.nth(i).text_content() or ""
                match = re.search(r'1\s+RSD\s*=\s*([\d,]+\.?\d*)', text, re.IGNORECASE)
                if match:
                    exchange_rate = float(match.group(1).replace(',', ''))
                    log_debug(f"      Extracted exchange rate: {exchange_rate}")
                    break
        except Exception as e:
            log_debug(f"      Failed to extract exchange rate: {e}")
        
        # Fallback calculation using base class method
        if exchange_rate == 0.0:
            exchange_rate = self.calculate_exchange_rate(converted_amount, original_amount)
            log_debug(f"      Calculated fallback exchange rate: {exchange_rate}")
        
        return converted_amount, exchange_rate
