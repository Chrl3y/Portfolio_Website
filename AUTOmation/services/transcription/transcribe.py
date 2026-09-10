"""
Transcription Service — wraps faster-whisper for the AUTOmation pipeline.

Usage:
    # As a CLI tool
    python transcribe.py input.m4a --model small --output transcript.json

    # Or as an importable module
    from services.transcription import transcribe

    result = transcribe("input.wav", model="small")

Output format:
{
  "language": "en",
  "language_probability": 0.99,
  "duration": 100,
  "segments": [{"start": 0.0, "end": 4.4, "text": "..."}],
  "full_text": "..."
}
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional

AUTO_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(AUTO_DIR))


def transcribe(
    input_path: str,
    model: str = "tiny",
    output_path: Optional[str] = None,
    beam_size: int = 5,
) -> dict:
    """
    Transcribe audio using faster-whisper.

    Args:
        input_path: Path to audio/video file
        model: Model name (tiny, tiny.en, base, small, medium, large-v2, etc.)
        output_path: Optional path to save JSON result
        beam_size: Beam size for decoding

    Returns:
        dict with language, segments, full_text, duration
    """
    from faster_whisper import WhisperModel

    print(f"Loading model: {model} (CPU mode)", file=sys.stderr)
    whisper_model = WhisperModel(model, device="cpu", compute_type="float32")

    print(f"Transcribing: {input_path}", file=sys.stderr)
    segments, info = whisper_model.transcribe(input_path, beam_size=beam_size)

    segment_list = []
    full_text_parts = []
    for segment in segments:
        segment_list.append({
            "start": round(segment.start, 3),
            "end": round(segment.end, 3),
            "text": segment.text,
        })
        full_text_parts.append(segment.text)

    result = {
        "language": info.language,
        "language_probability": round(info.language_probability, 4),
        "duration": round(info.duration, 3),
        "segments": segment_list,
        "full_text": "".join(full_text_parts),
        "model": model,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }

    if output_path:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"Saved transcript to: {output_path}", file=sys.stderr)

    return result


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio/video with faster-whisper")
    parser.add_argument("input", help="Input audio/video file path")
    parser.add_argument("--model", default="tiny", help="Model name (default: tiny)")
    parser.add_argument("--output", "-o", default=None, help="Output JSON file path")
    parser.add_argument("--beam-size", type=int, default=5, help="Beam size for decoding")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    result = transcribe(args.input, args.model, args.output, args.beam_size)

    # Print to stdout
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
