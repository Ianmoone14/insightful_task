import platform
from typing import Dict, Optional
from utils.logger import log_info, log_debug, log_error
from calculators.base_calculator import BaseCalculator


def detect_os() -> str:
    """
    Detect the current operating system.

    Returns:
        str: Operating system name (Windows, Linux, or macOS)
    """
    system = platform.system().lower()
    log_debug(f"Detected operating system: {system}")
    return system


def get_calculator_class() -> Optional[type[BaseCalculator]]:
    """
    Get the appropriate calculator class based on the operating system.

    Returns:
        Optional[type[BaseCalculator]]: Calculator class for the current OS
    """
    system = detect_os()

    if system == "windows":
        log_info("Initializing Windows Calculator service...")
        from calculators.windows_calculator import WindowsCalculator
        return WindowsCalculator
    elif system == "darwin":  # macOS
        log_info("Initializing macOS Calculator service...")
        # TODO: Implement macOS calculator when needed
        raise NotImplementedError("macOS calculator not yet implemented")
    elif system == "linux":
        log_info("Initializing Linux Calculator service...")
        from calculators.linux_calculator import LinuxCalculator
        return LinuxCalculator
    else:  # Default case for unknown systems
        log_error(f"Unsupported operating system: {system}")
        raise NotImplementedError(f"Calculator not implemented for {system}")

def get_required_packages() -> Dict[str, list[str]]:
    """
    Get the list of required packages for the current OS.

    Returns:
        Dict[str, list[str]]: Dictionary mapping OS names to their required packages
    """
    return {
        "linux": [
            "python3-pip",
            "python3-pyautogui",
            "python3-xlib",
            "wmctrl",
            "gnome-calculator",
            "xclip"
        ],
        "windows": [
            "pyautogui",
            "pyperclip"
        ],
        "darwin": [
            "pyautogui",
            "pyperclip"
        ]
    }


def get_os_specific_commands() -> Dict[str, list[str]]:
    """
    Get OS-specific commands that need to be run during installation.

    Returns:
        Dict[str, list[str]]: Dictionary mapping OS names to their required commands
    """
    return {
        "linux": [
            "sudo apt-get update",
            "sudo apt-get install -y python3-pip python3-pyautogui python3-xlib wmctrl gnome-calculator xclip",
            "pip3 install pyautogui pyperclip"
        ],
        "windows": [
            "pip install pyautogui pyperclip"
        ],
        "darwin": [
            "pip3 install pyautogui pyperclip"
        ]
    } 