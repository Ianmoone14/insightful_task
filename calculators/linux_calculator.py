
import subprocess
import time
import pyautogui
import pyperclip
from typing import Dict, List
from .base_calculator import BaseCalculator


class LinuxCalculator(BaseCalculator):
    """Linux calculator implementation using pyautogui for GUI automation."""

    # === Constants ===
    CALCULATOR_CMD = "gnome-calculator"
    CALCULATOR_KILL_CMD = "pkill"
    WINDOW_SEARCH_CMD = ["wmctrl", "-l", "-p"]
    WINDOW_ACTIVATE_CMD = "wmctrl"
    CALCULATOR_WINDOW_NAME = "Calculator"
    CALCULATOR_VERSION = "3.38.0"
    CALCULATOR_TYPE = "Scientific"

    def __init__(self):
        super().__init__()
        self.calculator_process = None

    def get_platform_name(self) -> str:
        return "Linux"

    def check_dependencies(self) -> bool:
        try:
            subprocess.run(['which', self.CALCULATOR_CMD], check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False

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

    def _open_calculator(self) -> None:
        try:
            subprocess.run([self.CALCULATOR_KILL_CMD, self.CALCULATOR_CMD], check=False)
            time.sleep(1)
            self.calculator_process = subprocess.Popen([self.CALCULATOR_CMD])
            time.sleep(2)

            window_list = subprocess.check_output(self.WINDOW_SEARCH_CMD).decode()
            calculator_window = None
            for line in window_list.split('\n'):
                if self.CALCULATOR_WINDOW_NAME in line:
                    calculator_window = line.split()[0]
                    break

            if not calculator_window:
                raise RuntimeError("Could not find calculator window")

            subprocess.run([self.WINDOW_ACTIVATE_CMD, "-ia", calculator_window], check=False)
            time.sleep(1)

            if self.calculator_process.poll() is not None:
                raise RuntimeError("Failed to start calculator")

        except Exception as e:
            raise Exception(f"Failed to open calculator: {str(e)}")

    def _close_calculator(self) -> None:
        if self.calculator_process:
            self.calculator_process.terminate()
            self.calculator_process = None
            time.sleep(1)

    def _perform_calculation(self, amount: float, rate: float) -> float:
        try:
            if self.calculator_process.poll() is not None:
                self._open_calculator()

            window_list = subprocess.check_output(self.WINDOW_SEARCH_CMD).decode()
            calculator_window = None
            for line in window_list.split('\n'):
                if self.CALCULATOR_WINDOW_NAME in line:
                    calculator_window = line.split()[0]
                    break

            if not calculator_window:
                raise RuntimeError("Could not find calculator window")

            subprocess.run([self.WINDOW_ACTIVATE_CMD, "-ia", calculator_window], check=False)
            time.sleep(1)

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(1)

            calculation = f"{amount}*{str(rate).replace('.', ',')}"
            pyautogui.write(calculation)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)

            pyperclip.copy('')
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)

            result = pyperclip.paste().strip()
            if not result:
                raise RuntimeError("No result copied from calculator")

            try:
                return float(result.replace(',', '.').replace(' ', ''))
            except Exception:
                raise RuntimeError(f"Failed to parse calculator result: {result}")

        except Exception as e:
            raise Exception(f"Failed to perform calculation: {str(e)}")

    def calculate(self, calculation: str) -> str:
        try:
            self._open_calculator()

            window_list = subprocess.check_output(self.WINDOW_SEARCH_CMD).decode()
            calculator_window = None
            for line in window_list.split('\n'):
                if self.CALCULATOR_WINDOW_NAME in line:
                    calculator_window = line.split()[0]
                    break

            if not calculator_window:
                raise RuntimeError("Could not find calculator window")

            subprocess.run([self.WINDOW_ACTIVATE_CMD, "-ia", calculator_window], check=False)
            time.sleep(1)

            pyautogui.hotkey('ctrl', 'a')
            pyautogui.press('delete')
            time.sleep(1)

            calculation = calculation.replace('.', ',')
            pyautogui.write(calculation)
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(2)

            pyperclip.copy('')
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)

            result = pyperclip.paste().strip()
            if not result:
                raise RuntimeError("No result copied from calculator")

            return result
        except Exception as e:
            raise Exception(f"Failed to perform calculation: {str(e)}")
        finally:
            self._close_calculator()

    def get_calculator_info(self) -> Dict[str, str]:
        return {
            "name": self.CALCULATOR_CMD,
            "version": self.CALCULATOR_VERSION,
            "type": self.CALCULATOR_TYPE
        }
