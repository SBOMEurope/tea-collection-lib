"""A generic include for all pytests.

Includes
- pytest fixtures that are used by many test files
"""
import pytest
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
