#!/usr/bin/env python3
"""
Create a ContentItem from environment variables (called by process-recording.sh).
"""

import sys
import os
import json
from pathlib import Path

# Add AUTOmation to path regardless of venv
AUTO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTO_DIR))

from services.content_store import ContentItem, ContentStore, init_db

# Ensure database exists
init_db()

content_id = os.environ["CONTENT_ID"]
input_path = os.environ["INPUT_PATH"]
title = os.environ.get("SCRIPT_TITLE", "Untitled Recording")
job_dir = os.environ["JOB_DIR"]

item = ContentItem(
    id=content_id,
    source_type="recording",
    source_path=input_path,
    title=title,
    classification="PRIVATE",
    approval_status="PENDING",
)
ContentStore.create(item)

source_meta = {
    "content_id": item.id,
    "source_type": item.source_type,
    "source_path": item.source_path,
    "title": item.title,
    "classification": item.classification,
    "created_at": item.created_at,
}

with open(os.path.join(job_dir, "source.json"), "w") as f:
    json.dump(source_meta, f, indent=2)

print(f"ContentItem created: {item.id}")
