"""
Cross-platform calculator implementations.

This package provides calculator services for different operating systems
using their native calculator applications.
"""

from .calculator_service import CalculatorService
from .base_calculator import BaseCalculator

__all__ = ['CalculatorService', 'BaseCalculator'] 