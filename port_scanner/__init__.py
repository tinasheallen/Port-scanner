"""
Port Scanner - A fast, multi-threaded port scanner.

This package provides functionality to scan multiple hosts and port ranges efficiently.
"""

__version__ = "1.0.0"

from .scanner import PortScanner, ScanResult

__all__ = ['PortScanner', 'ScanResult']
