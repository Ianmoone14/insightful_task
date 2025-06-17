from typing import List, Dict
from pages.xe_page import XEPage
from pages.wise_page import WisePage
from calculators import CalculatorService
from utils.file_writer import FileWriter
from utils.logger import log_info, log_debug


class CurrencyConverter:
    """Service to handle currency conversions from different sources."""
    
    def __init__(self, page):
        self.page = page
        self.file_writer = FileWriter()
        self.calculator = CalculatorService()
    
    def process_xe_conversions(self, amounts: List[float]):
        """Process XE.com conversions and add to consolidated file."""
        log_debug("Processing XE.com conversions...")
        xe_page = XEPage(self.page)
        
        # Get web conversions
        log_info("Getting XE.com currency conversions...")
        web_results = xe_page.get_rsd_conversions(amounts)
        web_data = self._structure_results(web_results, "XE.com")
        log_info(f"STRUCTURED WEB DATA - EUR Rate: {web_data['eur']['exchange_rate']:.10f}")
        log_info(f"STRUCTURED WEB DATA - USD Rate: {web_data['usd']['exchange_rate']:.10f}")
        
        # Close browser before calculator operations
        log_info("Closing browser...")
        self.page.context.close()
        
        # Get calculator conversions using rates from web
        log_info("Performing calculator conversions with XE rates...")
        eur_rate = web_data['eur']['exchange_rate']
        usd_rate = web_data['usd']['exchange_rate']
        log_info(f"RATES PASSED TO CALCULATOR - EUR: {eur_rate:.10f}")
        log_info(f"RATES PASSED TO CALCULATOR - USD: {usd_rate:.10f}")
        calculator_data = self.calculator.calculate_conversions(amounts, {"eur": eur_rate, "usd": usd_rate}, "Calculator")
        
        # Add to consolidated file
        self.file_writer.append_source_results("xe.com", web_data, calculator_data)
        log_info("XE.com results added to consolidated file")
        
        # Return data for verification
        return web_data, calculator_data
    
    def process_wise_conversions(self, amounts: List[float]):
        """Process Wise.com conversions and add to consolidated file."""
        log_debug("Processing Wise.com conversions...")
        wise_page = WisePage(self.page)
        
        # Get web conversions
        log_info("Getting Wise.com currency conversions...")
        web_results = wise_page.get_rsd_conversions(amounts)
        web_data = self._structure_results(web_results, "Wise.com")
        log_info(f"STRUCTURED WEB DATA - EUR Rate: {web_data['eur']['exchange_rate']:.10f}")
        log_info(f"STRUCTURED WEB DATA - USD Rate: {web_data['usd']['exchange_rate']:.10f}")
        
        # Close browser before calculator operations
        log_info("Closing browser...")
        self.page.context.close()
        
        # Get calculator conversions using rates from web
        log_info("Performing calculator conversions with Wise rates...")
        eur_rate = web_data['eur']['exchange_rate']
        usd_rate = web_data['usd']['exchange_rate']
        log_info(f"RATES PASSED TO CALCULATOR - EUR: {eur_rate:.10f}")
        log_info(f"RATES PASSED TO CALCULATOR - USD: {usd_rate:.10f}")
        calculator_data = self.calculator.calculate_conversions(amounts, {"eur": eur_rate, "usd": usd_rate}, "Calculator")
        
        # Add to consolidated file
        self.file_writer.append_source_results("wise.com", web_data, calculator_data)
        log_info("Wise.com results added to consolidated file")
        
        # Return data for verification
        return web_data, calculator_data
    
    def get_output_file_path(self) -> str:
        """Get the path to the consolidated output file."""
        return self.file_writer.get_consolidated_file_path()
    
    def _structure_results(self, results: List[Dict], source: str) -> Dict:
        """Structure results for easy comparison."""
        log_debug(f"Structuring {len(results)} results from {source}...")
        
        eur_results = [r for r in results if r["to_currency"] == "EUR"]
        usd_results = [r for r in results if r["to_currency"] == "USD"]
        
        # Use first exchange rate (should be same for all amounts from same source)
        eur_rate = eur_results[0]["exchange_rate"] if eur_results else 0
        usd_rate = usd_results[0]["exchange_rate"] if usd_results else 0
        
        log_debug(f"STRUCTURE RESULTS - Raw EUR rate from first result: {eur_rate:.10f}")
        log_debug(f"STRUCTURE RESULTS - Raw USD rate from first result: {usd_rate:.10f}")
        
        return {
            "source": source,
            "eur": {
                "exchange_rate": eur_rate,
                "conversions": {r["amount"]: r["converted_amount"] for r in eur_results}
            },
            "usd": {
                "exchange_rate": usd_rate,
                "conversions": {r["amount"]: r["converted_amount"] for r in usd_results}
            }
        } 