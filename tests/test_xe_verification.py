"""
XE.com Verification Test
Compares web scraping results against calculator results using same exchange rates.
"""

import pytest
from utils.currency_converter import CurrencyConverter
from utils.verification_service import VerificationService
from utils.logger import log_info


@pytest.mark.xe
class TestXEVerification:
    """Test class for XE.com verification against calculator accuracy."""

    def test_xe_verification_accuracy(self, page, test_data, verification_collector):
        """Test XE.com web scraping accuracy by comparing with calculator using same rates."""
        
        # Initialize services
        converter = CurrencyConverter(page)
        verification_service = VerificationService(tolerance=0.01)

        log_info("Starting XE.com verification test...")
        log_info(f"Testing with amounts: {test_data['amounts']} RSD")
        
        # Process XE.com conversions (web + calculator using XE rates) - this does everything
        log_info("Processing XE.com conversions...")
        web_data, calculator_data = converter.process_xe_conversions(test_data["amounts"])
        
        # Perform verification assertions
        log_info("Verifying web vs calculator results...")
        verification_service.assert_conversions_match(web_data, calculator_data, "XE.com")
        
        # Additional test assertions
        assert web_data["eur"]["exchange_rate"] > 0, "EUR exchange rate should be positive"
        assert web_data["usd"]["exchange_rate"] > 0, "USD exchange rate should be positive"
        assert len(web_data["eur"]["conversions"]) == len(test_data["amounts"]), "Should have EUR conversions for all amounts"
        assert len(web_data["usd"]["conversions"]) == len(test_data["amounts"]), "Should have USD conversions for all amounts"
        
        log_info("✓ XE.com verification test completed successfully!")
        log_info(f"Results saved to: {converter.get_output_file_path()}") 