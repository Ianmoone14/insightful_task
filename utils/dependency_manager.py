import os
import sys
import subprocess
from typing import Dict, List, Optional
from pathlib import Path
from utils.logger import log_info, log_error, log_debug
from utils.os_utils import detect_os, get_required_packages, get_os_specific_commands


class DependencyManager:
    """Manages installation and verification of project dependencies."""
    
    def __init__(self):
        self.os_name = detect_os()
        self.project_root = Path(__file__).parent.parent
        self.requirements_file = self.project_root / "requirements" / f"{self.os_name}.txt"
    
    def install_dependencies(self, force: bool = False) -> bool:
        """
        Install all required dependencies for the current OS.
        
        Args:
            force: If True, reinstall packages even if they're already installed
            
        Returns:
            bool: True if installation was successful
        """
        if not self.requirements_file.exists():
            log_error(f"No requirements file found for {self.os_name}")
            return False
        
        log_info(f"Installing dependencies for {self.os_name}...")
        
        # Install system packages
        if not self._install_system_packages(force):
            return False
        
        # Install Python packages
        if not self._install_python_packages(force):
            return False
        
        log_info("All dependencies installed successfully!")
        return True
    
    def verify_dependencies(self) -> Dict[str, bool]:
        """
        Verify that all required dependencies are installed.
        
        Returns:
            Dict[str, bool]: Dictionary mapping package names to their installation status
        """
        log_info(f"Verifying dependencies for {self.os_name}...")
        
        required_packages = get_required_packages().get(self.os_name, [])
        status = {}
        
        # Check system packages
        for package in required_packages:
            if not package.startswith("python"):
                try:
                    subprocess.run(['which', package], check=True, capture_output=True)
                    status[package] = True
                    log_debug(f"✓ {package} is installed")
                except subprocess.CalledProcessError:
                    status[package] = False
                    log_debug(f"✗ {package} is not installed")
        
        # Check Python packages
        python_packages = [pkg for pkg in required_packages if pkg.startswith("python") or pkg in ["pyautogui", "pyperclip"]]
        for package in python_packages:
            try:
                __import__(package.replace("python3-", "").replace("-", "_"))
                status[package] = True
                log_debug(f"✓ {package} is installed")
            except ImportError:
                status[package] = False
                log_debug(f"✗ {package} is not installed")
        
        return status
    
    def _install_system_packages(self, force: bool) -> bool:
        """Install system packages using the appropriate package manager."""
        os_commands = get_os_specific_commands().get(self.os_name, [])
        
        for command in os_commands:
            try:
                log_debug(f"Running command: {command}")
                subprocess.run(command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                log_error(f"Failed to run command: {command}")
                log_error(f"Error: {str(e)}")
                return False
        
        return True
    
    def _install_python_packages(self, force: bool) -> bool:
        """Install Python packages from requirements file."""
        if not self.requirements_file.exists():
            log_error(f"Requirements file not found: {self.requirements_file}")
            return False
        
        pip_cmd = "pip3" if sys.platform != "win32" else "pip"
        force_flag = "--force-reinstall" if force else ""
        
        try:
            log_debug(f"Installing Python packages from {self.requirements_file}")
            subprocess.run(
                f"{pip_cmd} install -r {self.requirements_file} {force_flag}",
                shell=True,
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            log_error(f"Failed to install Python packages")
            log_error(f"Error: {str(e)}")
            return False
    
    def get_missing_dependencies(self) -> List[str]:
        """
        Get a list of missing dependencies.
        
        Returns:
            List[str]: List of package names that are not installed
        """
        status = self.verify_dependencies()
        return [pkg for pkg, installed in status.items() if not installed]
    
    def is_fully_installed(self) -> bool:
        """
        Check if all dependencies are installed.
        
        Returns:
            bool: True if all dependencies are installed
        """
        return len(self.get_missing_dependencies()) == 0 