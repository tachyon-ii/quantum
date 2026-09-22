"""
Atomic Shell Modeller Package

A modular system for testing theories of electron shell configuration.
Follows clean architecture principles with separation of concerns.
"""

__version__ = "1.0.0"
__author__ = "Freeman Theory Research"

from .atom import Atom
from .data_loader import DataLoader
from .theory import FreemanTheory
from .modeller import AtomicModeller
from .validator import ConfigurationValidator

__all__ = [
    "Atom",
    "DataLoader", 
    "FreemanTheory",
    "AtomicModeller",
    "ConfigurationValidator"
]