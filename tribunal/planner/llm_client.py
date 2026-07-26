"""LLM Client module — Communicates with Ollama for query parsing."""

from __future__ import annotations

import json
import logging
from typing import Callable, Optional
import urllib.request
import urllib.error

from tribunal.planner.exceptions import LLMClientError
from tribunal.planner.prompts import QUERY_PLANNER_SYSTEM_PROMPT

logger = logging.getLogger("tribunal.planner.llm_client")


class LLMClient:
    """Client for communicating with Ollama inference engine.
    
    Does not parse JSON or validate AML intent; merely fetches raw response string.
    """

    def __init__(
        self,
        endpoint: str = "http://localhost:11434/api/generate",
        model: str = "llama3",
        timeout: float = 5.0,
        custom_caller: Optional[Callable[[str], str]] = None,
    ):
        self.endpoint = endpoint
        self.model = model
        self.timeout = timeout
        self.custom_caller = custom_caller

    def parse_query(self, query: str) -> str:
        """Send query prompt to LLM and return raw response string.
        
        Retries once on network failure or timeout before raising LLMClientError.
        """
        if not query or not query.strip():
            raise LLMClientError("Query string cannot be empty")

        prompt = f"{QUERY_PLANNER_SYSTEM_PROMPT}\n\nUser Query: {query.strip()}"
        logger.debug("Prompt sent to LLM: %s", prompt)

        if self.custom_caller is not None:
            try:
                res = self.custom_caller(query)
                logger.debug("Raw LLM response (custom caller): %s", res)
                return res
            except Exception as e:
                raise LLMClientError(f"Custom caller failed: {e}") from e

        payload = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }).encode("utf-8")

        # Retry loop (attempt twice)
        last_error = None
        for attempt in range(1, 3):
            try:
                req = urllib.request.Request(
                    self.endpoint,
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    if resp.status == 200:
                        body = json.loads(resp.read().decode("utf-8"))
                        response_text = body.get("response", "").strip()
                        if response_text:
                            logger.debug("Raw LLM response: %s", response_text)
                            return response_text
                        raise LLMClientError("LLM returned empty response body")
            except (urllib.error.URLError, TimeoutError, OSError) as err:
                last_error = err
                logger.warning(f"Ollama request attempt {attempt} failed: {err}")

        raise LLMClientError(f"Failed to connect to Ollama at {self.endpoint}: {last_error}")
