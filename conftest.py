"""Pytest configuration and pythonpath setup for TRIBUNAL."""

import sys
from pathlib import Path

# Add project root and tribunal package dir to sys.path
root_dir = Path(__file__).resolve().parent
tribunal_dir = root_dir / "tribunal"

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
if str(tribunal_dir) not in sys.path:
    sys.path.insert(0, str(tribunal_dir))
