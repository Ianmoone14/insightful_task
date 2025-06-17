import subprocess
import time
import pyperclip
from pywinauto import Application
from typing import Dict, List
from utils.logger import log_info, log_debug, log_error, log_warning
from .base_calculator import BaseCalculator


class WindowsCalculator(BaseCalculator):
    """Windows Calculator implementation using pywinauto."""

    # === UIA Locators ===
    LOCATOR_CLEAR_ENTRY = "clearEntryButton"
    LOCATOR_RESULTS = "CalculatorResults"
    CALCULATOR_TITLE = "Calculator"
    CALCULATOR_PROCESS = "CalculatorApp.exe"

    def __init__(self):
        super().__init__()
        self.app = None
        self.calculator = None

    def get_platform_name(self) -> str:
        return "Windows"

    def calculate_conversions(self, amounts: List[float], exchange_rates: Dict, source: str) -> Dict:
        calculator_results = self._create_results_structure(amounts, exchange_rates, source)
        self._open_calculator()
        try:
            self._log_calculation_start("EUR", exchange_rates['eur'])
            for amount in amounts:
                result = self._perform_calculation(amount, exchange_rates["eur"])
                calculator_results["eur"]["conversions"][amount] = result
                self._log_calculation_result(amount, exchange_rates['eur'], result, "EUR")

            self._log_calculation_start("USD", exchange_rates['usd'])
            for amount in amounts:
                result = self._perform_calculation(amount, exchange_rates["usd"])
                calculator_results["usd"]["conversions"][amount] = result
                self._log_calculation_result(amount, exchange_rates['usd'], result, "USD")
        finally:
            self._close_calculator()

        return calculator_results

    def _open_calculator(self):
        try:
            subprocess.run(['taskkill', '/f', '/im', self.CALCULATOR_PROCESS], capture_output=True, text=True)
            time.sleep(0.5)
            log_debug("Opening Windows Calculator...")
            subprocess.Popen(['calc.exe'])
            time.sleep(2)
            self.app = Application(backend="uia").connect(title=self.CALCULATOR_TITLE)
            self.calculator = self.app[self.CALCULATOR_TITLE]
            self.calculator.wait('ready', timeout=5)
            self.calculator_open = True
            log_info("Calculator connected successfully!")
        except Exception as e:
            log_error(f"Error opening calculator: {e}")
            log_warning("Trying alternative connection methods...")
            try:
                self.app = Application(backend="uia").connect(path=self.CALCULATOR_PROCESS)
                self.calculator = self.app.top_window()
                self.calculator_open = True
                log_info("Connected using alternative method!")
            except Exception as e2:
                log_error(f"Alternative connection failed: {e2}")
                self.calculator_open = False

    def _close_calculator(self):
        try:
            if self.calculator_open and self.calculator:
                log_debug("Closing Windows Calculator...")
                self.calculator.close()
            self.calculator_open = False
            self.app = None
            self.calculator = None
        except Exception as e:
            log_error(f"Error closing calculator: {e}")
            subprocess.run(['taskkill', '/f', '/im', self.CALCULATOR_PROCESS], capture_output=True, text=True)

    def _paste_number(self, number_str: str):
        try:
            pyperclip.copy(number_str)
            time.sleep(0.1)
            self.calculator.set_focus()
            time.sleep(0.1)
            self.calculator.type_keys("^v")
            time.sleep(0.15)
        except Exception as e:
            log_error(f"Error pasting number {number_str}: {e}")
            raise

    def _perform_calculation(self, amount: float, rate: float) -> float:
        try:
            if not self.calculator_open or not self.calculator:
                raise Exception("Calculator not properly initialized")

            log_debug(f"CALCULATOR INPUT - Amount: {amount}")
            log_debug(f"CALCULATOR INPUT - Rate: {rate:.10f}")

            try:
                self.calculator.type_keys("{ESC}")
                time.sleep(0.1)
            except Exception:
                try:
                    clear_button = self.calculator.child_window(auto_id=self.LOCATOR_CLEAR_ENTRY)
                    clear_button.click_input()
                    time.sleep(0.1)
                except Exception:
                    log_warning("Unable to clear calculator. Proceeding anyway.")

            self._paste_number(str(int(amount)))
            self.calculator.type_keys("*")
            time.sleep(0.1)
            self._paste_number(f"{rate:.10f}")
            self.calculator.type_keys("{ENTER}")
            time.sleep(0.2)

            try:
                display = self.calculator.child_window(auto_id=self.LOCATOR_RESULTS)
                result_text = display.window_text().strip()
                if result_text:
                    result_value = float(result_text.replace(",", "").replace("Display is", "").strip())
                    log_debug(f"CALCULATOR RESULT - Got from display: {result_value:.8f}")
                    return result_value
            except Exception as display_error:
                log_warning(f"Failed to read result from display: {display_error}")

            try:
                self.calculator.type_keys("^c")
                time.sleep(0.15)
                clipboard_text = pyperclip.paste().strip()
                if clipboard_text:
                    return float(clipboard_text.replace(",", ""))
                raise Exception("Empty clipboard result")
            except Exception as clipboard_error:
                log_error(f"Clipboard fallback failed: {clipboard_error}")

            raise Exception("Failed to read result from UI")

        except Exception as e:
            log_error(f"Calculation error: {e}")