"""
Content Store — SQLite schema and initialization for AUTOmation.

Database: AUTOmation/runtime/data/automation.db
"""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "runtime" / "data" / "automation.db"

SCHEMA = """
-- Main content items table
CREATE TABLE IF NOT EXISTS content_items (
    id              TEXT PRIMARY KEY,
    source_type     TEXT NOT NULL,          -- recording, note, github_repo, etc.
    source_path     TEXT NOT NULL,
    title           TEXT,
    classification  TEXT NOT NULL DEFAULT 'PRIVATE',   -- PRIVATE, REVIEW, PUBLIC
    approval_status TEXT NOT NULL DEFAULT 'PENDING',    -- PENDING, APPROVED, REJECTED
    confidentiality_checked BOOLEAN NOT NULL DEFAULT 0,
    editorial_script TEXT,                 -- cleaned/edited script
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL
);

-- Transcripts from transcription engines
CREATE TABLE IF NOT EXISTS transcripts (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    engine          TEXT NOT NULL,          -- faster-whisper, whisperx
    language        TEXT,
    language_probability REAL,
    duration        REAL,
    full_text       TEXT,
    segments_json   TEXT,                   -- JSON array of {start, end, text}
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Scene plans generated from transcripts
CREATE TABLE IF NOT EXISTS scene_plans (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    plan_json       TEXT NOT NULL,          -- conforms to video-scene-plan.schema.json
    rendering_status TEXT DEFAULT 'pending', -- pending, rendered, failed
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Media assets (rendered videos, images, cleaned audio)
CREATE TABLE IF NOT EXISTS media_assets (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT,                   -- NULL for reusable assets
    type            TEXT NOT NULL,          -- render, cover, thumbnail, audio_clean, audio_original
    path            TEXT NOT NULL,
    format          TEXT,                   -- mp4, mp3, png, etc.
    width           INTEGER,
    height          INTEGER,
    duration        REAL,
    size_bytes      INTEGER,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE SET NULL
);

-- Publishing jobs (Postiz/Ayrshare/etc.)
CREATE TABLE IF NOT EXISTS publication_jobs (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    target_platform TEXT NOT NULL,          -- postiz, ayrshare, vizard
    status          TEXT NOT NULL,          -- pending, draft_created, published, failed
    remote_id       TEXT,                   -- ID on the publishing platform
    publish_at      TEXT,                   -- ISO datetime or NULL for immediate
    error_message   TEXT,
    created_at      TEXT NOT NULL,
    updated_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Approval audit trail
CREATE TABLE IF NOT EXISTS approvals (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    actor           TEXT NOT NULL,          -- 'charles' in single-user mode
    action          TEXT NOT NULL,          -- APPROVE, REJECT, CLASSIFY, MAKE_PRIVATE
    previous_status TEXT,
    new_status      TEXT,
    notes           TEXT,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Analytics events (views, engagement, etc.)
CREATE TABLE IF NOT EXISTS analytics_events (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    event_type      TEXT NOT NULL,          -- view, click, share, publish
    platform        TEXT,                   -- twitter, linkedin, portfolio, etc.
    metadata_json   TEXT,
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Affiliate candidate tracking
CREATE TABLE IF NOT EXISTS affiliate_candidates (
    id              TEXT PRIMARY KEY,
    content_item_id TEXT NOT NULL,
    product_name    TEXT NOT NULL,
    affiliate_url    TEXT NOT NULL,
    commission_rate REAL,                   -- e.g. 0.05 for 5%
    relevance_score REAL,                   -- 0.0 to 1.0
    status          TEXT NOT NULL DEFAULT 'candidate', -- candidate, inserted, rejected
    created_at      TEXT NOT NULL,
    FOREIGN KEY (content_item_id) REFERENCES content_items(id) ON DELETE CASCADE
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_content_items_title ON content_items(title);
CREATE INDEX IF NOT EXISTS idx_content_items_classification ON content_items(classification);
CREATE INDEX IF NOT EXISTS idx_content_items_approval ON content_items(approval_status);
CREATE INDEX IF NOT EXISTS idx_transcripts_content ON transcripts(content_item_id);
CREATE INDEX IF NOT EXISTS idx_scene_plans_content ON scene_plans(content_item_id);
CREATE INDEX IF NOT EXISTS idx_media_content ON media_assets(content_item_id);
CREATE INDEX IF NOT EXISTS idx_pub_jobs_content ON publication_jobs(content_item_id);
CREATE INDEX IF NOT EXISTS idx_approvals_content ON approvals(content_item_id);
CREATE INDEX IF NOT EXISTS idx_analytics_content ON analytics_events(content_item_id);
CREATE INDEX IF NOT EXISTS idx_affiliate_content ON affiliate_candidates(content_item_id);
"""


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


if __name__ == "__main__":
    init_db()
