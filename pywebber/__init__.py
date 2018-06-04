"""Python Web Tools"""
import os, sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from .lorem import LoremPysum
from .indexing import add_page_to_index
from .ripper import Ripper
from .utils import unique_everseen


__all__ = ["LoremPysum", "Ripper", "add_page_to_index", "unique_everseen"]
