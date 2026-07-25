"""Unit tests for QueryParser."""

import pytest
from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.models.user_query import UserQuery
from tribunal.planner.exceptions import QueryParseError, ValidationError
from tribunal.planner.query_parser import QueryParser


def test_parse_valid_json_manual_c11_spec():
    parser = QueryParser()
    json_input = """
    {
      "intent": "pattern_detection",
      "pattern": "structuring",
      "filters": {
        "date_range": "last_30_days"
      },
      "output": "investigation_report"
    }
    """
    plan = parser.parse_json(json_input)

    assert isinstance(plan, InvestigationPlan)
    assert plan.intent == "pattern_detection"
    assert plan.target_pattern == "structuring"
    assert plan.filters == {"date_range": "last_30_days"}
    assert plan.requested_output == "investigation_report"
    assert plan.experts == ["financial", "behaviour"]
    assert plan.run_eda is True


def test_parse_markdown_code_block():
    parser = QueryParser()
    json_markdown = """```json
    {
      "intent": "behaviour_analysis",
      "entities": ["ACC123"],
      "filters": {"risk_level": "high"}
    }
    ```"""
    plan = parser.parse(json_markdown)
    assert plan.intent == "behaviour_analysis"
    assert plan.entities == ["ACC123"]
    assert plan.customer_id == "ACC123"
    assert plan.experts == ["behaviour"]


def test_parse_reject_unknown_intent():
    parser = QueryParser()
    json_input = '{"intent": "unknown_super_intent"}'
    with pytest.raises(ValidationError, match="Unknown intent"):
        parser.parse_json(json_input)


def test_parse_reject_unknown_pattern():
    parser = QueryParser()
    json_input = '{"intent": "pattern_detection", "pattern": "invalid_pattern_xyz"}'
    with pytest.raises(ValidationError, match="Unknown pattern"):
        parser.parse_json(json_input)


def test_parse_reject_malformed_json():
    parser = QueryParser()
    with pytest.raises(QueryParseError, match="Malformed JSON"):
        parser.parse_json("{intent: pattern_detection")


def test_parse_empty_query():
    parser = QueryParser()
    with pytest.raises(ValidationError, match="cannot be empty"):
        parser.parse("")


def test_rule_based_fallback_parsing():
    parser = QueryParser()
    plan = parser.parse_text("Find structuring deposits in last month")
    assert plan.intent == "pattern_detection"
    assert plan.target_pattern == "structuring"
    assert plan.filters.get("date_range") == "last_30_days"
