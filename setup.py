from setuptools import setup, find_packages

setup(
    name="insightful",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.40.0",
        "pytest>=7.4.0", 
        "pytest-playwright>=0.4.0",
        "pyautogui>=0.9.50",
        "pyperclip>=1.8.0",
        "pywinauto>=0.6.8",
    ],
    python_requires=">=3.8",
) 