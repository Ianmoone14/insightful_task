import os
from datetime import datetime
from typing import Dict
from utils.logger import log_info


class FileWriter:
    """Utility for writing consolidated results to one file."""
    
    def __init__(self):
        # Only create reports directory for the single output file
        os.makedirs("reports", exist_ok=True)
        self.consolidated_path = None
    
    def initialize_consolidated_file(self) -> str:
        """Initialize the consolidated results file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"currency_conversion_results_{timestamp}.txt"
        self.consolidated_path = os.path.join("reports", filename)
        
        with open(self.consolidated_path, 'w', encoding='utf-8') as f:
            f.write("")  # Start with empty file
        
        log_info(f"Initialized consolidated results file: {self.consolidated_path}")
        return self.consolidated_path
    
    def append_source_results(self, source: str, web_data: Dict, calculator_data: Dict):
        """Append results for a source to the consolidated file."""
        if not self.consolidated_path:
            self.initialize_consolidated_file()
        
        with open(self.consolidated_path, 'a', encoding='utf-8') as f:
            f.write(f"=== Source: {source.lower()} ===\n")
            f.write(f"Exchange Rate (EUR): {web_data['eur']['exchange_rate']:.8f}\n")
            f.write(f"Exchange Rate (USD): {web_data['usd']['exchange_rate']:.8f}\n\n")
            
            f.write("Website Conversions:\n")
            for amount in sorted(web_data['eur']['conversions'].keys()):
                eur_converted = web_data['eur']['conversions'][amount]
                usd_converted = web_data['usd']['conversions'].get(amount, 0)
                f.write(f"Value in RSD: {amount}\n")
                f.write(f"→ EUR: {eur_converted:.2f}\n")
                f.write(f"→ USD: {usd_converted:.2f}\n")
                f.write("...\n\n")
            
            f.write("Calculator Conversions:\n")
            for amount in sorted(calculator_data['eur']['conversions'].keys()):
                eur_converted = calculator_data['eur']['conversions'][amount]
                usd_converted = calculator_data['usd']['conversions'].get(amount, 0)
                f.write(f"Value in RSD: {amount}\n")
                f.write(f"→ EUR: {eur_converted:.2f}\n")
                f.write(f"→ USD: {usd_converted:.2f}\n")
                f.write("...\n\n")
            
            f.write("-" * 31 + "\n\n")
        
        log_info(f"Appended {source} results to consolidated file")
    
    def get_consolidated_file_path(self) -> str:
        """Get the path to the consolidated file."""
        return self.consolidated_path
