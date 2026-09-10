"""
Content API — FastAPI service for managing ContentItem objects.

Endpoints:
    GET  /health
    POST /content
    GET  /content
    GET  /content/{id}
    PATCH /content/{id}
    POST /content/{id}/approve
    POST /content/{id}/reject
    POST /content/{id}/classify
    GET  /content/{id}/transcript
    GET  /content/{id}/scene-plan
    GET  /content/{id}/media
    GET  /content/{id}/publications
"""

import sys
import os
from pathlib import Path

# Add AUTOmation to path for imports
AUTOmation_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(AUTOmation_DIR))

from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

from services.content_store import init_db, ContentItem, ContentStore

init_db()

app = FastAPI(title="AUTOmation Content API", version="1.0.0")


# --- Pydantic models ---

class CreateContentRequest(BaseModel):
    source_type: str
    source_path: str
    title: Optional[str] = None
    classification: str = "PRIVATE"

class ClassifyRequest(BaseModel):
    classification: str

class ApprovalRequest(BaseModel):
    actor: str = "charles"
    notes: Optional[str] = None


# --- Routes ---

@app.get("/health")
def health():
    return {"status": "healthy", "service": "content-api", "timestamp": datetime.now().isoformat()}


@app.post("/content")
def create_content(req: CreateContentRequest):
    item = ContentItem.create(
        source_type=req.source_type,
        source_path=req.source_path,
        title=req.title,
        classification=req.classification,
    )
    ContentStore.create(item)
    return item.to_dict()


@app.get("/content")
def list_content():
    conn = __import__("services.content_store", fromlist=["get_db"]).get_db()
    rows = conn.execute("SELECT * FROM content_items ORDER BY created_at DESC").fetchall()
    conn.close()
    items = []
    for row in rows:
        items.append(ContentItem(
            id=row["id"], source_type=row["source_type"], source_path=row["source_path"],
            title=row["title"], classification=row["classification"],
            approval_status=row["approval_status"],
            confidentiality_checked=bool(row["confidentiality_checked"]),
            editorial_script=row["editorial_script"],
            created_at=row["created_at"], updated_at=row["updated_at"],
        ).to_dict())
    return {"items": items}


@app.get("/content/{item_id}")
def get_content(item_id: str):
    item = ContentStore.get(item_id)
    if item is None:
        raise HTTPException(404, f"ContentItem {item_id} not found")
    return item.to_dict()


@app.patch("/content/{item_id}")
def update_content(item_id: str, updates: dict = Body(...)):
    item = ContentStore.update(item_id, **updates)
    if item is None:
        raise HTTPException(404, f"ContentItem {item_id} not found")
    return item.to_dict()


@app.post("/content/{item_id}/approve")
def approve_content(item_id: str, req: ApprovalRequest = Body(...)):
    item = ContentStore.approve(item_id, actor=req.actor, notes=req.notes)
    if item is None:
        raise HTTPException(404, f"ContentItem {item_id} not found")
    return item.to_dict()


@app.post("/content/{item_id}/reject")
def reject_content(item_id: str, req: ApprovalRequest = Body(...)):
    item = ContentStore.reject(item_id, actor=req.actor, notes=req.notes)
    if item is None:
        raise HTTPException(404, f"ContentItem {item_id} not found")
    return item.to_dict()


@app.post("/content/{item_id}/classify")
def classify_content(item_id: str, req: ClassifyRequest):
    item = ContentStore.classify(item_id, req.classification)
    if item is None:
        raise HTTPException(404, f"ContentItem {item_id} not found")
    return item.to_dict()


@app.get("/content/{item_id}/transcript")
def get_transcript(item_id: str):
    conn = __import__("services.content_store", fromlist=["get_db"]).get_db()
    row = conn.execute(
        "SELECT * FROM transcripts WHERE content_item_id = ? ORDER BY created_at DESC LIMIT 1",
        (item_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(404, f"No transcript for content item {item_id}")
    return dict(row)


@app.get("/content/{item_id}/scene-plan")
def get_scene_plan(item_id: str):
    conn = __import__("services.content_store", fromlist=["get_db"]).get_db()
    row = conn.execute(
        "SELECT * FROM scene_plans WHERE content_item_id = ? ORDER BY created_at DESC LIMIT 1",
        (item_id,)
    ).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(404, f"No scene plan for content item {item_id}")
    return dict(row)


@app.get("/content/{item_id}/media")
def get_media(item_id: str):
    conn = __import__("services.content_store", fromlist=["get_db"]).get_db()
    rows = conn.execute(
        "SELECT * FROM media_assets WHERE content_item_id = ? ORDER BY created_at DESC",
        (item_id,)
    ).fetchall()
    conn.close()
    return {"assets": [dict(r) for r in rows]}


@app.get("/content/{item_id}/publications")
def get_publications(item_id: str):
    conn = __import__("services.content_store", fromlist=["get_db"]).get_db()
    rows = conn.execute(
        "SELECT * FROM publication_jobs WHERE content_item_id = ? ORDER BY created_at DESC",
        (item_id,)
    ).fetchall()
    conn.close()
    return {"publications": [dict(r) for r in rows]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8010)
