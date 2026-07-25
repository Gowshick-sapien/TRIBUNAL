"""TRIBUNAL package initialization."""

from tribunal.consensus.tribunal import Tribunal
from tribunal.report.report_generator import ReportGenerator

__version__ = "1.0.0"

__all__ = ["Tribunal", "ReportGenerator", "__version__"]
