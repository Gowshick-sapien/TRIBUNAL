"""Phase C.7 — Investigation Report & Explainability Engine package."""

from tribunal.report.explainability_engine import ExplainabilityEngine
from tribunal.report.renderer_html import HTMLRenderer
from tribunal.report.renderer_json import JSONRenderer
from tribunal.report.renderer_markdown import MarkdownRenderer
from tribunal.report.report_builder import ReportBuilder
from tribunal.report.report_generator import ReportGenerator
from tribunal.report.report_validator import ReportValidator, ReportValidationError

__all__ = [
    "ReportGenerator",
    "ReportBuilder",
    "ExplainabilityEngine",
    "MarkdownRenderer",
    "HTMLRenderer",
    "JSONRenderer",
    "ReportValidator",
    "ReportValidationError",
]
