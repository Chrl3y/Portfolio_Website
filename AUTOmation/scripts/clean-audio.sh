#!/bin/bash
# AUTOmation — clean-audio.sh
# Noise reduction wrapper around DeepFilterNet.
#
# Usage:
#   ./scripts/clean-audio.sh <input.wav> [output_dir]
#
# Purpose:
#   recorded voice -> noise reduction -> clean narration
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTO_DIR="$(dirname "$SCRIPT_DIR")"
ENV_DIR="$AUTO_DIR/deepfilternet-env"

INPUT="${1:-}"
OUTPUT_DIR="${2:-}"

if [[ -z "$INPUT" ]]; then
    echo "Usage: ./scripts/clean-audio.sh <input.wav> [output_dir]"
    exit 1
fi

if [[ ! -f "$INPUT" ]]; then
    echo "Error: input file not found: $INPUT"
    exit 1
fi

if [[ -z "$OUTPUT_DIR" ]]; then
    OUTPUT_DIR="$(dirname "$INPUT")"
fi

if [[ ! -d "$ENV_DIR" ]]; then
    echo "Error: DeepFilterNet venv not found at $ENV_DIR"
    echo "Create it: uv venv deepfilternet-env && source deepfilternet-env/bin/activate && uv pip install deepfilternet"
    exit 1
fi

# Activate venv and run DeepFilterNet CLI
source "$ENV_DIR/bin/activate"
deep-filter-py "$INPUT" --output-dir "$OUTPUT_DIR" 2>&1

echo "Done: cleaned file in $OUTPUT_DIR"
