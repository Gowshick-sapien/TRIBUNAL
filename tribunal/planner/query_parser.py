"""Query Parser module — Parses, validates, and normalizes raw LLM output or JSON into InvestigationPlan."""

from __future__ import annotations

import json
import re
from typing import Any

from tribunal.models.investigation_plan import InvestigationPlan
from tribunal.models.user_query import UserQuery
from tribunal.planner.exceptions import QueryParseError, ValidationError
from tribunal.planner.planner_constants import (
    BEHAVIOUR,
    BEHAVIOUR_ANALYSIS,
    CASE_SUMMARY,
    CUSTOMER_LOOKUP,
    EDA_REQUEST,
    FINANCIAL,
    INVESTIGATION_REPORT,
    NETWORK_ANALYSIS,
    PATTERN_DETECTION,
    SUPPORTED_INTENTS,
    SUPPORTED_OUTPUTS,
    SUPPORTED_PATTERNS,
)


class QueryParser:
    """Transforms raw LLM output or query text into a validated InvestigationPlan.
    
    Ensures no dictionaries leave this module; returns only InvestigationPlan domain objects.
    """

    def parse(self, query_input: UserQuery | str | dict) -> InvestigationPlan:
        """Parse input (UserQuery object, raw JSON string, or dict) into InvestigationPlan."""
        if isinstance(query_input, UserQuery):
            raw_text = query_input.text
        elif isinstance(query_input, str):
            raw_text = query_input
        elif isinstance(query_input, dict):
            return self._build_plan_from_dict(query_input, raw_query="")
        else:
            raise ValidationError(f"Unsupported query input type: {type(query_input)}")

        if not raw_text or not raw_text.strip():
            raise ValidationError("Query text cannot be empty")

        # Try parsing raw_text as JSON
        try:
            data = self._clean_and_parse_json(raw_text)
            return self._build_plan_from_dict(data, raw_query=raw_text)
        except (QueryParseError, json.JSONDecodeError):
            # Fallback to rule-based parser if raw text is natural language rather than JSON
            return self.parse_text_rule_based(raw_text)

    def parse_json(self, json_str: str, raw_query: str = "") -> InvestigationPlan:
        """Explicitly parse a JSON string into an InvestigationPlan."""
        if not json_str or not json_str.strip():
            raise QueryParseError("JSON string cannot be empty")
        data = self._clean_and_parse_json(json_str)
        return self._build_plan_from_dict(data, raw_query=raw_query or json_str)

    def parse_text(self, query_text: str) -> InvestigationPlan:
        """Convenience method accepting raw query string."""
        return self.parse(query_text)

    def parse_text_rule_based(self, text: str) -> InvestigationPlan:
        """Rule-based regex parser fallback for natural language text when LLM JSON is unavailable."""
        text_lower = text.lower().strip()
        if not text_lower:
            raise ValidationError("Query text cannot be empty")

        # Intent detection
        if "eda" in text_lower or "distribution" in text_lower or "statistics" in text_lower:
            intent = EDA_REQUEST
        elif "summary" in text_lower or "summarize" in text_lower:
            intent = CASE_SUMMARY
        elif "network" in text_lower or "graph" in text_lower or "topology" in text_lower:
            intent = NETWORK_ANALYSIS
        elif ("structuring" in text_lower or "velocity" in text_lower or "transfer" in text_lower) and ("behaviour" in text_lower or "behavior" in text_lower):
            intent = PATTERN_DETECTION
        elif "structuring" in text_lower or "pattern" in text_lower:
            intent = PATTERN_DETECTION
        elif "behaviour" in text_lower or "behavior" in text_lower or "dormant" in text_lower:
            intent = BEHAVIOUR_ANALYSIS
        elif "investigate account" in text_lower or "investigate customer" in text_lower or "customer" in text_lower:
            intent = CUSTOMER_LOOKUP
        else:
            intent = PATTERN_DETECTION

        # Pattern detection
        pattern = None
        for p in SUPPORTED_PATTERNS:
            if p.replace("_", " ") in text_lower or p in text_lower:
                pattern = p
                break
        if "deposits" in text_lower or "deposit" in text_lower:
            pattern = pattern or "structuring"

        # Entity extraction
        entities = []
        acc_match = re.search(r"(?:account|acc(?:ount)?|customer|user)\s+([A-Za-z0-9_-]+)", text, re.IGNORECASE)
        if not acc_match:
            acc_match = re.search(r"\b(ACC_[A-Za-z0-9_-]+)\b", text)
        if not acc_match:
            stop_words = {"investigate", "structuring", "behaviour", "behavior", "anomalies", "transaction", "transactional", "financial", "customer"}
            fallback_matches = re.findall(r"\b([0-9A-Za-z]{8,15})\b", text)
            for cand in fallback_matches:
                if cand.lower() not in stop_words and any(c.isdigit() for c in cand):
                    entities.append(cand)
                    break
        elif acc_match and intent in (CUSTOMER_LOOKUP, BEHAVIOUR_ANALYSIS, PATTERN_DETECTION):
            entities.append(acc_match.group(1))

        # Filters
        filters: dict[str, Any] = {}
        if "last month" in text_lower or "30 days" in text_lower:
            filters["date_range"] = "last_30_days"

        return self._build_plan(
            raw_query=text,
            intent=intent,
            pattern=pattern,
            entities=entities,
            filters=filters,
            requested_output=INVESTIGATION_REPORT,
        )

    def _clean_and_parse_json(self, raw_str: str) -> dict[str, Any]:
        """Strip markdown wrappers and parse JSON string."""
        cleaned = raw_str.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r"\s*```$", "", cleaned)
            cleaned = cleaned.strip()

        try:
            parsed = json.loads(cleaned)
            if not isinstance(parsed, dict):
                raise QueryParseError("LLM response must be a JSON object")
            return parsed
        except json.JSONDecodeError as err:
            raise QueryParseError(f"Malformed JSON: {err}") from err

    def _build_plan_from_dict(self, data: dict[str, Any], raw_query: str) -> InvestigationPlan:
        """Validate dict schema and values, then construct InvestigationPlan."""
        intent = data.get("intent")
        if not intent:
            raise ValidationError("Missing required key 'intent' in planner output")
        
        # Normalize string values
        intent = str(intent).lower().strip()
        if intent not in SUPPORTED_INTENTS:
            raise ValidationError(f"Unknown intent: '{intent}'. Supported: {sorted(SUPPORTED_INTENTS)}")

        pattern = data.get("pattern")
        if pattern:
            pattern = str(pattern).lower().strip()
            if pattern not in SUPPORTED_PATTERNS:
                raise ValidationError(f"Unknown pattern: '{pattern}'. Supported: {sorted(SUPPORTED_PATTERNS)}")

        requested_output = data.get("requested_output") or data.get("output") or INVESTIGATION_REPORT
        requested_output = str(requested_output).lower().strip()
        if requested_output not in SUPPORTED_OUTPUTS:
            raise ValidationError(f"Unknown output format: '{requested_output}'. Supported: {sorted(SUPPORTED_OUTPUTS)}")

        entities = data.get("entities") or []
        if isinstance(entities, str):
            entities = [entities]
        elif not isinstance(entities, list):
            raise ValidationError("Key 'entities' must be a list of strings")

        filters = data.get("filters") or {}
        if not isinstance(filters, dict):
            raise ValidationError("Key 'filters' must be a dictionary")

        return self._build_plan(
            raw_query=raw_query or json.dumps(data),
            intent=intent,
            pattern=pattern,
            entities=[str(e) for e in entities],
            filters=filters,
            requested_output=requested_output,
        )

    def _build_plan(
        self,
        raw_query: str,
        intent: str,
        pattern: str | None,
        entities: list[str],
        filters: dict[str, Any],
        requested_output: str,
    ) -> InvestigationPlan:
        """Map intent to experts and construct domain InvestigationPlan."""
        experts: list[str] = []
        run_eda = False

        if intent in (PATTERN_DETECTION, CUSTOMER_LOOKUP):
            experts = [FINANCIAL, BEHAVIOUR]
            run_eda = True
        elif intent == BEHAVIOUR_ANALYSIS:
            experts = [BEHAVIOUR]
            run_eda = True
        elif intent == EDA_REQUEST:
            experts = []
            run_eda = True
        elif intent in (NETWORK_ANALYSIS, CASE_SUMMARY):
            experts = []
            run_eda = False

        customer_id = entities[0] if entities else None

        return InvestigationPlan(
            raw_query=raw_query,
            intent=intent,
            experts=experts,
            run_eda=run_eda,
            target_pattern=pattern,
            customer_id=customer_id,
            entities=entities,
            filters=filters,
            requested_output=requested_output,
        )
