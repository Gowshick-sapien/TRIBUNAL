"""Search Repository module — Advanced SQL search, similarity ranking, bookmarks & tag annotations."""

from __future__ import annotations

import csv
import datetime
import io
import json
import logging
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from storage.database import DatabaseManager, DEFAULT_DB_PATH
from storage.models import InvestigationRecord

logger = logging.getLogger("tribunal.storage.repositories.search")


@dataclass
class SearchResultItem:
    """SearchResultItem dataclass returning rich metadata."""
    id: str
    created_at: str
    query: str
    dataset: str
    planner_intent: str
    risk_level: str
    confidence: float
    recommendation: str
    status: str
    duration_ms: float
    version: str
    winning_hypothesis: Optional[str] = None
    is_bookmarked: bool = False
    tags: List[str] = field(default_factory=list)
    node_count: int = 0
    edge_count: int = 0


@dataclass
class SimilarInvestigationItem:
    """Dataclass holding similarity rank results."""
    item: SearchResultItem
    similarity_score: float
    similarity_reasons: List[str]


class SearchRepository:
    """Repository handling search, filtering, similarity analysis, bookmarks, and tag annotations."""

    def __init__(self, db_manager: Optional[DatabaseManager] = None) -> None:
        self.db_manager = db_manager or DatabaseManager(DEFAULT_DB_PATH)

    def search(
        self,
        query: Optional[str] = None,
        risk_level: Optional[str] = None,
        min_confidence: Optional[float] = None,
        max_confidence: Optional[float] = None,
        dataset: Optional[str] = None,
        status: Optional[str] = None,
        expert: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        only_bookmarked: bool = False,
        sort_by: str = "newest",  # 'newest', 'oldest', 'confidence_desc', 'risk_desc', 'fastest'
        limit: int = 20,
        offset: int = 0,
    ) -> Tuple[List[SearchResultItem], int]:
        """Execute multi-criteria SQL metadata query with pagination."""
        where_clauses = ["1=1"]
        params: List[Any] = []

        if query and query.strip():
            q_clean = f"%{query.strip()}%"
            where_clauses.append(
                "(i.query LIKE ? OR i.planner_intent LIKE ? OR i.id LIKE ? OR v.winning_hypothesis LIKE ? OR i.recommendation LIKE ?)"
            )
            params.extend([q_clean, q_clean, q_clean, q_clean, q_clean])

        if risk_level and risk_level.upper() != "ALL":
            where_clauses.append("i.risk_level = ?")
            params.append(risk_level.upper())

        if min_confidence is not None:
            where_clauses.append("i.confidence >= ?")
            params.append(float(min_confidence))

        if max_confidence is not None:
            where_clauses.append("i.confidence <= ?")
            params.append(float(max_confidence))

        if dataset and dataset.lower() != "all":
            where_clauses.append("i.dataset = ?")
            params.append(dataset)

        if status and status.lower() != "all":
            where_clauses.append("i.status = ?")
            params.append(status.upper())

        if start_date:
            where_clauses.append("i.created_at >= ?")
            params.append(start_date)

        if end_date:
            where_clauses.append("i.created_at <= ?")
            params.append(end_date)

        if only_bookmarked:
            where_clauses.append("b.investigation_id IS NOT NULL")

        where_sql = " AND ".join(where_clauses)

        # Sorting logic
        order_map = {
            "newest": "i.created_at DESC",
            "oldest": "i.created_at ASC",
            "confidence_desc": "i.confidence DESC",
            "confidence_asc": "i.confidence ASC",
            "risk_desc": "CASE i.risk_level WHEN 'CRITICAL' THEN 4 WHEN 'HIGH' THEN 3 WHEN 'MEDIUM' THEN 2 ELSE 1 END DESC",
            "fastest": "i.duration_ms ASC",
        }
        order_sql = order_map.get(sort_by, "i.created_at DESC")

        sql = f"""
            SELECT 
                i.id, i.created_at, i.query, i.dataset, i.planner_intent, i.risk_level,
                i.confidence, i.recommendation, i.status, i.duration_ms, i.version,
                v.winning_hypothesis,
                g.node_count, g.edge_count,
                CASE WHEN b.investigation_id IS NOT NULL THEN 1 ELSE 0 END AS is_bookmarked
            FROM investigations i
            LEFT JOIN verdicts v ON i.id = v.investigation_id
            LEFT JOIN graphs g ON i.id = g.investigation_id
            LEFT JOIN bookmarks b ON i.id = b.investigation_id
            WHERE {where_sql}
            ORDER BY {order_sql}
            LIMIT ? OFFSET ?
        """

        count_sql = f"""
            SELECT COUNT(DISTINCT i.id)
            FROM investigations i
            LEFT JOIN verdicts v ON i.id = v.investigation_id
            LEFT JOIN bookmarks b ON i.id = b.investigation_id
            WHERE {where_sql}
        """

        try:
            with self.db_manager.get_connection() as conn:
                # Count total matching
                cur = conn.execute(count_sql, params)
                total = cur.fetchone()[0]

                # Fetch items
                fetch_params = params + [limit, offset]
                rows = conn.execute(sql, fetch_params).fetchall()

                items: List[SearchResultItem] = []
                for row in rows:
                    inv_id = row["id"]
                    # Fetch tags for each item
                    tag_rows = conn.execute("SELECT tag FROM tags WHERE investigation_id = ?", (inv_id,)).fetchall()
                    tags = [t["tag"] for t in tag_rows]

                    item = SearchResultItem(
                        id=inv_id,
                        created_at=row["created_at"],
                        query=row["query"],
                        dataset=row["dataset"],
                        planner_intent=row["planner_intent"],
                        risk_level=row["risk_level"],
                        confidence=float(row["confidence"]),
                        recommendation=row["recommendation"],
                        status=row["status"],
                        duration_ms=float(row["duration_ms"]),
                        version=row["version"],
                        winning_hypothesis=row["winning_hypothesis"],
                        is_bookmarked=bool(row["is_bookmarked"]),
                        tags=tags,
                        node_count=int(row["node_count"] or 0),
                        edge_count=int(row["edge_count"] or 0),
                    )
                    items.append(item)

                return items, total
        except sqlite3.Error as e:
            logger.error(f"Search SQL query failed: {e}")
            return [], 0

    def get_recent(self, limit: int = 10) -> List[SearchResultItem]:
        """Fetch most recently executed investigations."""
        items, _ = self.search(sort_by="newest", limit=limit)
        return items

    def get_bookmarked(self) -> List[SearchResultItem]:
        """Fetch bookmarked investigations."""
        items, _ = self.search(only_bookmarked=True, limit=100)
        return items

    def toggle_bookmark(self, investigation_id: str, notes: Optional[str] = None) -> bool:
        """Toggle bookmark status for an investigation ID. Returns True if now bookmarked, False if removed."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            with self.db_manager.get_connection() as conn:
                cur = conn.execute("SELECT 1 FROM bookmarks WHERE investigation_id = ?", (investigation_id,))
                exists = cur.fetchone() is not None
                if exists:
                    conn.execute("DELETE FROM bookmarks WHERE investigation_id = ?", (investigation_id,))
                    conn.commit()
                    return False
                else:
                    conn.execute(
                        "INSERT INTO bookmarks (investigation_id, created_at, notes) VALUES (?, ?, ?)",
                        (investigation_id, now, notes or ""),
                    )
                    conn.commit()
                    return True
        except sqlite3.Error as e:
            logger.error(f"Failed to toggle bookmark for '{investigation_id}': {e}")
            return False

    def add_tag(self, investigation_id: str, tag: str) -> bool:
        """Add custom user tag annotation."""
        clean_tag = tag.strip()
        if not clean_tag:
            return False
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    "INSERT OR IGNORE INTO tags (investigation_id, tag, created_at) VALUES (?, ?, ?)",
                    (investigation_id, clean_tag, now),
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to add tag '{tag}' to '{investigation_id}': {e}")
            return False

    def remove_tag(self, investigation_id: str, tag: str) -> bool:
        """Remove custom user tag annotation."""
        try:
            with self.db_manager.get_connection() as conn:
                conn.execute(
                    "DELETE FROM tags WHERE investigation_id = ? AND tag = ?",
                    (investigation_id, tag.strip()),
                )
                conn.commit()
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to remove tag '{tag}' from '{investigation_id}': {e}")
            return False

    def get_similar(self, investigation_id: str, limit: int = 5) -> List[SimilarInvestigationItem]:
        """Metadata Similarity Engine ranking historical investigations."""
        # 1. Fetch target investigation
        items, _ = self.search(limit=1, offset=0)
        target_list = [i for i in self.get_recent(limit=100) if i.id == investigation_id]
        if not target_list:
            return []
        target = target_list[0]

        # 2. Fetch candidates excluding target
        all_candidates = [i for i in self.get_recent(limit=100) if i.id != investigation_id]

        similar_items: List[SimilarInvestigationItem] = []
        for cand in all_candidates:
            score = 0.0
            reasons = []

            # Match 1: Planner Intent / Category Overlap
            if cand.planner_intent and target.planner_intent and cand.planner_intent == target.planner_intent:
                score += 0.35
                reasons.append(f"Identical planner intent pattern '{cand.planner_intent}'")

            # Match 2: Winning Hypothesis Similarity
            if cand.winning_hypothesis and target.winning_hypothesis:
                ch = cand.winning_hypothesis.lower()
                th = target.winning_hypothesis.lower()
                if ch == th:
                    score += 0.35
                    reasons.append(f"Matching winning hypothesis: '{cand.winning_hypothesis}'")
                elif any(word in th for word in ch.split()):
                    score += 0.20
                    reasons.append("Overlapping hypothesis domain")

            # Match 3: Risk Level Proximity
            if cand.risk_level == target.risk_level:
                score += 0.15
                reasons.append(f"Same risk level classification ({target.risk_level})")

            # Match 4: Confidence Proximity
            if abs(cand.confidence - target.confidence) <= 0.15:
                score += 0.15
                reasons.append(f"Close confidence score ({cand.confidence:.2f} vs {target.confidence:.2f})")

            if score > 0.10:
                similar_items.append(
                    SimilarInvestigationItem(
                        item=cand,
                        similarity_score=round(score, 2),
                        similarity_reasons=reasons,
                    )
                )

        similar_items.sort(key=lambda x: x.similarity_score, reverse=True)
        return similar_items[:limit]

    def export_csv(self, items: List[SearchResultItem]) -> str:
        """Format search result items as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Created At", "Query", "Dataset", "Planner Intent",
            "Risk Level", "Confidence", "Verdict/Hypothesis", "Recommendation", "Status", "Duration (ms)"
        ])
        for item in items:
            writer.writerow([
                item.id,
                item.created_at,
                item.query,
                item.dataset,
                item.planner_intent,
                item.risk_level,
                item.confidence,
                item.winning_hypothesis or "N/A",
                item.recommendation,
                item.status,
                item.duration_ms,
            ])
        return output.getvalue()
