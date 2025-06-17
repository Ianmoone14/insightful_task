from playwright.sync_api import Page
from typing import Dict, List
import re


class BasePage:
    """Base page with common currency conversion logic."""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate_to(self, url: str) -> None:
        """Navigate to URL without sleeps."""
        self.page.goto(url, timeout=30000)
        self.page.wait_for_load_state("domcontentloaded")
    
    def create_result(self, amount: float, from_currency: str, to_currency: str, 
                     converted_amount: float, exchange_rate: float, source: str) -> Dict:
        """Create standardized result dictionary."""
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "converted_amount": converted_amount,
            "exchange_rate": exchange_rate,
            "source": source
        }
    
    def calculate_exchange_rate(self, converted_amount: float, original_amount: float) -> float:
        """Calculate exchange rate from amounts."""
        if converted_amount > 0 and original_amount > 0:
            return converted_amount / original_amount
        return 0.0
    
    def extract_number_from_text(self, text: str) -> float:
        """Extract numeric value from text."""
        if not text:
            return 0.0
        clean_text = text.replace(',', '').replace(' ', '')
        match = re.search(r'([\d.]+)', clean_text)
        return float(match.group(1)) if match else 0.0
    
    def get_rsd_conversions(self, amounts: List[float]) -> List[Dict]:
        """Template method - to be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_rsd_conversions") 