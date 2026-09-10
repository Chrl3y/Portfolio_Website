#!/bin/bash
# AUTOmation — prepare-audio.sh
# Deterministic audio preprocessing pipeline for the content factory.
#
# Usage:
#   ./scripts/prepare-audio.sh <input.m4a|input.mp4|input.wav> <output_dir> [--denoise]
#
# Pipeline:
#   source recording → ffmpeg extraction → WAV (16kHz mono) → [optional DeepFilterNet] → loudness normalization → clean.wav
#
# Outputs:
#   <output_dir>/audio-original.wav  (extracted, never overwritten)
#   <output_dir>/audio-clean.wav     (processed)
#
set -euo pipefail

AUTO_DIR="/Users/Chuck/REPOS/projects/Portfolio_Website_v2/AUTOmation"
cd "$AUTO_DIR" || exit 1

INPUT="${1:-}"
OUTPUT_DIR="${2:-/tmp/automation-audio}"
DENOISE="${3:-}"

if [ -z "$INPUT" ]; then
  echo "Usage: $0 <input.m4a|input.mp4|input.wav> <output_dir> [--denoise]"
  echo ""
  echo "Pipeline: source → ffmpeg extract → WAV(16kHz mono) → [optional DeepFilterNet] → loudness normalize → clean.wav"
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "ERROR: Input file not found: $INPUT"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "=== AUTOmation Audio Preparation ==="
echo "Input:  $INPUT"
echo "Output: $OUTPUT_DIR"
echo ""

# Step 1: Extract original audio as WAV (16kHz mono)
echo "[1/4] Extracting audio → audio-original.wav"
ffmpeg -y -i "$INPUT" \
  -ar 16000 \
  -ac 1 \
  -sample_fmt s16 \
  "$OUTPUT_DIR/audio-original.wav" 2>&1 | tail -3

# Step 2: Optional DeepFilterNet denoising
if [ "$DENOISE" = "--denoise" ]; then
  echo "[2/4] DeepFilterNet denoising → audio-clean.wav (pre-denoise)"
  source "$AUTO_DIR/runtime/deepfilternet-env/bin/activate"
  deep-filter-py "$OUTPUT_DIR/audio-original.wav" --output-dir "$OUTPUT_DIR" --no-df-stage 2>&1 | tail -5 || {
  echo "WARNING: DeepFilterNet failed, falling back to original"
  cp "$OUTPUT_DIR/audio-original.wav" "$OUTPUT_DIR/audio-clean.wav"
  }
  deactivate
else
  echo "[2/4] Skipping denoise (no --denoise flag)"
  cp "$OUTPUT_DIR/audio-original.wav" "$OUTPUT_DIR/audio-clean.wav"
fi

# Step 3: Loudness normalization (target -16 LUFS for speech, -14 for music)
echo "[3/4] Loudness normalization → audio-clean.wav"
ffmpeg -y -i "$OUTPUT_DIR/audio-clean.wav" \
  -af "loudnorm=I=-16:TP=-1.5:LRA=11" \
  "$OUTPUT_DIR/audio-clean-norm.wav" 2>&1 | tail -3

# Use normalized as clean
mv "$OUTPUT_DIR/audio-clean-norm.wav" "$OUTPUT_DIR/audio-clean.wav"

# Step 4: Verify output
echo "[4/4] Verification"
ffprobe -v error -show_entries format=duration,format_name -of default=noprint_wrappers=1 "$OUTPUT_DIR/audio-clean.wav"

echo ""
echo "=== Done ==="
echo "Original: $OUTPUT_DIR/audio-original.wav"
echo "Clean:   $OUTPUT_DIR/audio-clean.wav"
