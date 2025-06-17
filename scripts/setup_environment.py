#!/usr/bin/env python3
"""
Complete environment setup script for currency conversion tests.
Handles everything needed so you can just run: pytest tests/
"""

import subprocess
import sys
import platform
import os


def print_header():
    """Print setup header."""
    print("=" * 60)
    print("CURRENCY CONVERSION TEST ENVIRONMENT SETUP")
    print("=" * 60)
    print(f"Operating System: {platform.system()}")
    print(f"Python Version: {platform.python_version()}")
    print("")


def run_command(command, description, critical=True, show_output=False):
    """Run a command and handle errors."""
    print(f"- {description}...")
    try:
        if show_output:
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"  SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  FAILED")
        if not show_output:
            print(f"  Output:\n{e.stdout}\n{e.stderr}")
        if critical:
            print(f"  Setup cannot continue")
            sys.exit(1)
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"  Python {version.major}.{version.minor} is compatible")
        return True
    else:
        print(f"  Python {version.major}.{version.minor} is too old. Need Python 3.8+")
        sys.exit(1)


def install_linux_system_packages():
    """Install Linux system packages."""
    if platform.system() != "Linux":
        return True

    print("\nLINUX SYSTEM PACKAGES")
    print("-" * 30)

    # Remove CD-ROM source if it exists
    run_command("sudo sed -i '/cdrom:/d' /etc/apt/sources.list", "Removing CD-ROM source", critical=False)

    # Update package list
    if not run_command("sudo apt-get update", "Updating package list", critical=False):
        print("  Warning: Package list update failed, but continuing with installation")

    packages = [
        "python3-venv", "python3-pip", "python3-tk",
        "gnome-calculator", "wmctrl", "xclip"
    ]

    package_list = " ".join(packages)
    if not run_command(f"sudo apt-get install -y {package_list}", "Installing system packages", critical=False):
        print("  Warning: Some packages could not be installed")
        return False

    print("Linux system packages installed")
    return True


def create_virtual_environment():
    """Create and setup virtual environment."""
    print("\nVIRTUAL ENVIRONMENT")
    print("-" * 30)

    if os.path.exists(".venv"):
        print("Virtual environment already exists - using existing one")
        return True

    python_cmd = "python" if platform.system() == "Windows" else "python3"
    run_command(f"{python_cmd} -m venv .venv", "Creating virtual environment")

    print("Virtual environment created")
    return True


def install_python_packages():
    """Install Python packages in virtual environment."""
    print("\nPYTHON PACKAGES")
    print("-" * 30)

    if platform.system() == "Windows":
        pip_cmd = ".venv\\Scripts\\pip"
        python_cmd = ".venv\\Scripts\\python"
    else:
        pip_cmd = ".venv/bin/pip"
        python_cmd = ".venv/bin/python"

    run_command(f"{python_cmd} -m pip install --upgrade pip", "Upgrading pip")
    run_command(f"{pip_cmd} install -r requirements.txt", "Installing Python packages")

    print("Python packages installed")
    return True


def install_playwright_browser():
    """Install Playwright browser."""
    print("\nBROWSER SETUP")
    print("-" * 30)

    if platform.system() == "Windows":
        playwright_cmd = ".venv\\Scripts\\playwright"
    else:
        playwright_cmd = ".venv/bin/playwright"

    run_command(f"{playwright_cmd} install chromium", "Installing Chromium browser")

    print("Browser installed")
    return True


def create_runner_scripts():
    """Create convenient runner scripts."""
    print("\nCREATING RUNNER SCRIPTS")
    print("-" * 30)

    if platform.system() == "Windows":
        # Create Windows batch file
        batch_content = """@echo off
echo.
echo Activating virtual environment...
call .venv\\Scripts\\activate.bat
echo Running tests...
echo.
python -m pytest tests/ -v --headed
echo.
"""
        with open("run_tests.bat", "w") as f:
            f.write(batch_content)
        print("- Created run_tests.bat")

    else:
        # Create Linux shell script
        shell_content = """#!/bin/bash
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate
echo "Running tests..."
echo ""
python -m pytest tests/ -v --headed
"""
        with open("run_tests.sh", "w") as f:
            f.write(shell_content)
        os.chmod("run_tests.sh", 0o755)
        print("- Created run_tests.sh")


def verify_installation():
    """Verify that everything is installed correctly."""
    print("\nVERIFICATION")
    print("-" * 30)

    if platform.system() == "Windows":
        python_cmd = ".venv\\Scripts\\python"
    else:
        python_cmd = ".venv/bin/python"

    # Simple verification - just check if we can import pytest
    try:
        subprocess.run(f'{python_cmd} -c "import pytest"', shell=True, check=True, capture_output=True)
        print("- Virtual environment is working correctly")
    except:
        print("- Warning: Could not verify installation")


def show_next_steps():
    """Show what to do next."""
    print("\n" + "=" * 60)
    print("SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 60)

    print("\nTO RUN TESTS:")

    if platform.system() == "Windows":
        print("  run_tests.bat")
        print("\n  Manual:")
        print("    .venv\\Scripts\\activate")
        print("    pytest tests/")

    else:
        print("  ./run_tests.sh")
        print("\n  Manual:")
        print("    source .venv/bin/activate")
        print("    pytest tests/")

    print("\nResults will be saved in: reports/")
    print("\nEverything is ready!")


def main():
    """Main setup function."""
    try:
        print_header()
        check_python_version()
        install_linux_system_packages()
        create_virtual_environment()
        install_python_packages()
        install_playwright_browser()
        create_runner_scripts()
        verify_installation()
        show_next_steps()

    except KeyboardInterrupt:
        print("\nSetup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 