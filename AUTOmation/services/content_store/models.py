"""
Content Store — model and data access for ContentItem objects.
"""

import uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional
from .database import get_db

@dataclass
class ContentItem:
    id: str
    source_type: str
    source_path: str
    title: Optional[str] = None
    classification: str = "PRIVATE"      # PRIVATE, REVIEW, PUBLIC
    approval_status: str = "PENDING"     # PENDING, APPROVED, REJECTED
    confidentiality_checked: bool = False
    editorial_script: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @staticmethod
    def create(source_type: str, source_path: str, title: Optional[str] = None,
               classification: str = "PRIVATE") -> "ContentItem":
        return ContentItem(
            id=f"c_{uuid.uuid4().hex[:12]}",
            source_type=source_type,
            source_path=source_path,
            title=title,
            classification=classification,
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "source_type": self.source_type,
            "source_path": self.source_path,
            "title": self.title,
            "classification": self.classification,
            "approval_status": self.approval_status,
            "confidentiality_checked": self.confidentiality_checked,
            "editorial_script": self.editorial_script,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class ContentStore:
    @staticmethod
    def create(item: ContentItem) -> ContentItem:
        conn = get_db()
        conn.execute(
            "INSERT INTO content_items (id, source_type, source_path, title, "
            "classification, approval_status, confidentiality_checked, editorial_script, "
            "created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (item.id, item.source_type, item.source_path, item.title,
             item.classification, item.approval_status, int(item.confidentiality_checked),
             item.editorial_script, item.created_at, item.updated_at),
        )
        conn.commit()
        conn.close()
        return item

    @staticmethod
    def get(item_id: str) -> Optional[ContentItem]:
        conn = get_db()
        row = conn.execute(
            "SELECT * FROM content_items WHERE id = ?", (item_id,)
        ).fetchone()
        conn.close()
        if row is None:
            return None
        return ContentItem(
            id=row["id"],
            source_type=row["source_type"],
            source_path=row["source_path"],
            title=row["title"],
            classification=row["classification"],
            approval_status=row["approval_status"],
            confidentiality_checked=bool(row["confidentiality_checked"]),
            editorial_script=row["editorial_script"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    @staticmethod
    def update(item_id: str, **fields) -> Optional[ContentItem]:
        if not fields:
            return ContentStore.get(item_id)
        # Convert Python booleans to SQLite integers
        for key, value in fields.items():
            if isinstance(value, bool):
                fields[key] = int(value)
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        values = list(fields.values()) + [datetime.now(timezone.utc).isoformat(), item_id]
        conn = get_db()
        conn.execute(
            f"UPDATE content_items SET {set_clause}, updated_at = ? WHERE id = ?",
            values,
        )
        conn.commit()
        conn.close()
        return ContentStore.get(item_id)

    @staticmethod
    def approve(item_id: str, actor: str = "charles", notes: Optional[str] = None) -> Optional[ContentItem]:
        item = ContentStore.get(item_id)
        if item is None:
            return None
        old_status = item.approval_status
        conn = get_db()
        conn.execute(
            "INSERT INTO approvals (id, content_item_id, actor, action, previous_status, new_status, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"app_{uuid.uuid4().hex[:12]}", item_id, actor, "APPROVE", old_status, "APPROVED", notes,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.execute(
            "UPDATE content_items SET approval_status = ?, updated_at = ? WHERE id = ?",
            ("APPROVED", datetime.now(timezone.utc).isoformat(), item_id),
        )
        conn.commit()
        conn.close()
        return ContentStore.get(item_id)

    @staticmethod
    def reject(item_id: str, actor: str = "charles", notes: Optional[str] = None) -> Optional[ContentItem]:
        item = ContentStore.get(item_id)
        if item is None:
            return None
        old_status = item.approval_status
        conn = get_db()
        conn.execute(
            "INSERT INTO approvals (id, content_item_id, actor, action, previous_status, new_status, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"app_{uuid.uuid4().hex[:12]}", item_id, actor, "REJECT", old_status, "REJECTED", notes,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.execute(
            "UPDATE content_items SET approval_status = ?, updated_at = ? WHERE id = ?",
            ("REJECTED", datetime.now(timezone.utc).isoformat(), item_id),
        )
        conn.commit()
        conn.close()
        return ContentStore.get(item_id)

    @staticmethod
    def classify(item_id: str, classification: str, actor: str = "charles",
                 notes: Optional[str] = None) -> Optional[ContentItem]:
        item = ContentStore.get(item_id)
        if item is None:
            return None
        old_classification = item.classification
        conn = get_db()
        conn.execute(
            "INSERT INTO approvals (id, content_item_id, actor, action, previous_status, new_status, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"app_{uuid.uuid4().hex[:12]}", item_id, actor, "CLASSIFY", old_classification, classification, notes,
             datetime.now(timezone.utc).isoformat()),
        )
        conn.execute(
            "UPDATE content_items SET classification = ?, updated_at = ? WHERE id = ?",
            (classification, datetime.now(timezone.utc).isoformat(), item_id),
        )
        conn.commit()
        conn.close()
        return ContentStore.get(item_id)

    @staticmethod
    def can_publish(item_id: str) -> tuple[bool, str]:
        """
        Safety gate before any publishing API call.

        Returns (allowed: bool, reason: str)
        """
        item = ContentStore.get(item_id)
        if item is None:
            return False, f"ContentItem {item_id} not found"

        if item.classification == "PRIVATE":
            return False, "Classification is PRIVATE"

        if item.approval_status != "APPROVED":
            return False, f"Approval status is {item.approval_status}, not APPROVED"

        if not item.confidentiality_checked:
            return False, "Confidentiality not checked"

        return True, "Approved for publishing"
