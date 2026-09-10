#!/usr/bin/env python3
"""
Generate a scene plan from a transcript (rule-based first version).
Called by process-recording.sh.

Input: JOB_DIR/transcript.json
Output: JOB_DIR/scene-plan.json
"""

import sys
import os
import json
from pathlib import Path

# Add AUTOmation to path regardless of venv
AUTO_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTO_DIR))

content_id = os.environ["CONTENT_ID"]
job_dir = os.environ["JOB_DIR"]

with open(os.path.join(job_dir, "transcript.json")) as f:
    transcript = json.load(f)

segments = transcript.get("segments", [])
full_text = transcript.get("full_text", "")

scene_plan = {
    "schema": "video-scene-plan",
    "version": "1.0",
    "content_id": content_id,
    "scenes": [],
    "duration": transcript.get("duration", 0),
}

# Title scene
if segments:
    scene_plan["scenes"].append({
        "type": "title",
        "renderer": "remotion",
        "duration": min(4.0, segments[0]["start"]),
        "content": {
            "title": full_text[:60] + "..." if len(full_text) > 60 else full_text,
        }
    })

# Text scenes from segments
for seg in segments:
    scene_type = "kinetic-text" if len(seg["text"]) < 100 else "original-camera"
    renderer = "remotion" if scene_type == "kinetic-text" else "manim"
    scene_plan["scenes"].append({
        "type": scene_type,
        "renderer": renderer,
        "start": seg["start"],
        "end": seg["end"],
        "content": {
            "text": seg["text"].strip(),
        }
    })

# CTA at end
scene_plan["scenes"].append({
    "type": "cta",
    "renderer": "remotion",
    "duration": 3.0,
    "content": {
        "text": "Subscribe for more content",
    }
})

with open(os.path.join(job_dir, "scene-plan.json"), "w") as f:
    json.dump(scene_plan, f, indent=2)

print(f"Scene plan: {len(scene_plan['scenes'])} scenes")
