#!/bin/bash
# AUTOmation — process-recording.sh
# First end-to-end content factory pipeline.
#
# Usage:
#   ./scripts/process-recording.sh <recording.m4a|recording.mp4> [--denoise]
#
set -euo pipefail

AUTO_DIR="/Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation"
cd "$AUTO_DIR" || exit 1

INPUT="${1:-}"
DENOISE="${2:-}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <recording.m4a|recording.mp4> [--denoise]"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "ERROR: Input file not found: $INPUT"
  exit 1
fi

SCRIPT_NAME=$(basename "$INPUT")
SCRIPT_TITLE="${SCRIPT_NAME%.*}"
CONTENT_ID="c_$(date +%s)_$(echo "$INPUT" | md5sum | cut -d' ' -f1 | head -c8)"
JOB_DIR="$AUTO_DIR/runtime/jobs/$CONTENT_ID"

echo "=== AUTOmation Process Recording ==="
echo "Content ID: $CONTENT_ID"
echo "Job Dir:    $JOB_DIR"
echo "Input:      $INPUT"
echo ""

mkdir -p "$JOB_DIR/renders"

# Step 1: Audio preparation
echo "[1/7] Audio Preparation"
"$AUTO_DIR/scripts/prepare-audio.sh" "$INPUT" "$JOB_DIR" $DENOISE
echo ""

# Step 2: Transcription
echo "[2/7] Transcription (faster-whisper, small model)"
source "$AUTO_DIR/runtime/faster-whisper-env/bin/activate"
python "$AUTO_DIR/services/transcription/transcribe.py" \
  "$JOB_DIR/audio-clean.wav" \
  --model small \
  --output "$JOB_DIR/transcript.json" 2>&1 | tail -10
deactivate
echo ""

# Step 3: Create ContentItem
echo "[3/7] Creating ContentItem (SQLite)"
CONTENT_ID="$CONTENT_ID" \
INPUT_PATH="$INPUT" \
SCRIPT_TITLE="$SCRIPT_TITLE" \
JOB_DIR="$JOB_DIR" \
"$AUTO_DIR/runtime/faster-whisper-env/bin/python" "$AUTO_DIR/scripts/create-content-item.py"
echo ""

# Step 4: Generate captions
echo "[4/7] Caption Generation"
"$AUTO_DIR/runtime/faster-whisper-env/bin/python" "$AUTO_DIR/services/captions/generate.py" \
  "$JOB_DIR/transcript.json" \
  --output-dir "$JOB_DIR" 2>&1
echo ""

# Step 5: Scene planning (rule-based)
echo "[5/7] Scene Planning"
CONTENT_ID="$CONTENT_ID" \
JOB_DIR="$JOB_DIR" \
"$AUTO_DIR/runtime/faster-whisper-env/bin/python" "$AUTO_DIR/scripts/generate-scene-plan.py" 2>&1
echo ""

# Step 6: Rendering (manual for now)
echo "[6/7] Rendering"
echo "  Manual step: run Remotion/Manim renders based on scene-plan.json"
echo ""

# Step 7: Assembly (manual for now)
echo "[7/7] Assembly"
echo "  Manual step: run FFmpeg assembly"
echo ""

# Save job metadata
"$AUTO_DIR/runtime/faster-whisper-env/bin/python" -c "
import json, os
job = {
    'content_id': '$CONTENT_ID',
    'input': '$INPUT',
    'status': 'completed',
    'steps': {
        'audio_prep': 'done',
        'transcription': 'done',
        'content_item': 'done',
        'captions': 'done',
        'scene_plan': 'done',
        'rendering': 'pending',
        'assembly': 'pending'
    },
    'output_dir': '$JOB_DIR'
}
with open('$JOB_DIR/job.json', 'w') as f:
    json.dump(job, f, indent=2)
print(f'Job metadata saved: $JOB_DIR/job.json')
" 2>&1

echo ""
echo "=== Pipeline Complete ==="
echo "Job directory: $JOB_DIR"
echo "Next steps: review scene-plan.json, render scenes, assemble video"
echo "Content item is PRIVATE + PENDING — must be APPROVED before any publishing."
