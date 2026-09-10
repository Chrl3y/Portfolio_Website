"""
Caption Generator — produces SRT, VTT, and JSON captions from transcript data.

Input: transcript JSON (from transcription service)
Output:
  - captions.srt
  - captions.vtt
  - captions.json
  - short-form chunks (for social clips)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Optional
from datetime import timedelta


def format_timestamp_srt(seconds: float) -> str:
    """Format seconds as SRT timestamp: HH:MM:SS,mmm"""
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    hours, remainder = divmod(total_ms, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"


def format_timestamp_vtt(seconds: float) -> str:
    """Format seconds as VTT timestamp: HH:MM:SS.mmm"""
    td = timedelta(seconds=seconds)
    total_ms = int(td.total_seconds() * 1000)
    hours, remainder = divmod(total_ms, 3600000)
    minutes, remainder = divmod(remainder, 60000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{ms:03d}"


def escape_html(text: str) -> str:
    """Escape HTML entities for VTT safety."""
    return (text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def split_text(text: str, max_chars: int = 60) -> list[str]:
    """Split text to fit within max_chars per line (approximate for 16:9 display)."""
    words = text.strip().split()
    if not words:
        return []
    lines = []
    current = ""
    for word in words:
        if len(current + " " + word) <= max_chars:
            current = (current + " " + word).strip()
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines if lines else [text]


def generate_srt(segments: list[dict], max_chars: int = 60) -> str:
    """Generate SRT content from transcript segments."""
    srt = []
    idx = 1
    for seg in segments:
        lines = split_text(seg["text"], max_chars)
        if len(lines) > 2:
            lines = [seg["text"]] if len(seg["text"]) <= max_chars * 2 else lines[:2]

        srt.append(str(idx))
        srt.append(f"{format_timestamp_srt(seg['start'])} --> {format_timestamp_srt(seg['end'])}")
        srt.extend(lines)
        srt.append("")
        idx += 1
    return "\n".join(srt)


def generate_vtt(segments: list[dict], max_chars: int = 60) -> str:
    """Generate VTT content from transcript segments."""
    vtt = ["WEBVTT"]
    for seg in segments:
        lines = split_text(seg["text"], max_chars)
        if len(lines) > 2:
            lines = [seg["text"]] if len(seg["text"]) <= max_chars * 2 else lines[:2]

        vtt.append(f"{format_timestamp_vtt(seg['start'])} --> {format_timestamp_vtt(seg['end'])}")
        vtt.extend(lines)
        vtt.append("")
    return "\n".join(vtt)


def generate_json(segments: list[dict]) -> str:
    """Generate JSON captions."""
    return json.dumps({"captions": segments}, indent=2)


def generate_short_form_chunks(segments: list[dict], target_duration: float = 55.0,
                                max_chars: int = 180) -> list[dict]:
    """
    Split transcript into short-form chunks (~55 seconds, 180 chars) suitable for social clips.
    Each chunk includes emphasis markers for key words.
    """
    chunks = []
    current_text = ""
    current_start = None
    current_end = None

    for seg in segments:
        seg_text = seg["text"].strip()
        if not seg_text:
            continue

        if current_start is None:
            current_start = seg["start"]

        if len(current_text + " " + seg_text) > max_chars or (seg["end"] - current_start > target_duration):
            if current_text.strip():
                emphasis = []
                for word in current_text.split():
                    if len(word) > 6 and word[0].isupper():
                        emphasis.append(word.rstrip(".,!?"))
                chunks.append({
                    "start": round(current_start, 3),
                    "end": round(current_end, 3),
                    "text": current_text.strip(),
                    "emphasis": emphasis[:5],
                })
            current_text = seg_text
            current_start = seg["start"]
        else:
            if current_text:
                current_text += " "
            current_text += seg_text

        current_end = seg["end"]

    if current_text.strip():
        emphasis = []
        for word in current_text.split():
            if len(word) > 6 and word[0].isupper():
                emphasis.append(word.rstrip(".,!?"))
        chunks.append({
            "start": round(current_start, 3),
            "end": round(current_end, 3),
            "text": current_text.strip(),
            "emphasis": emphasis[:5],
        })

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Generate captions from transcript JSON")
    parser.add_argument("transcript", help="Path to transcript JSON file")
    parser.add_argument("--output-dir", "-o", default=".", help="Output directory")
    parser.add_argument("--max-chars", type=int, default=60, help="Max chars per caption line")
    parser.add_argument("--chunk-duration", type=float, default=55.0, help="Short-form chunk duration")
    parser.add_argument("--chunk-chars", type=int, default=180, help="Short-form chunk max chars")

    args = parser.parse_args()

    with open(args.transcript) as f:
        transcript = json.load(f)

    segments = transcript.get("segments", [])
    if not segments:
        print("WARNING: No segments in transcript", file=sys.stderr)
        segments = []

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # SRT
    srt_content = generate_srt(segments, args.max_chars)
    (output_dir / "captions.srt").write_text(srt_content)
    print(f"Written: {output_dir / 'captions.srt'}")

    # VTT
    vtt_content = generate_vtt(segments, args.max_chars)
    (output_dir / "captions.vtt").write_text(vtt_content)
    print(f"Written: {output_dir / 'captions.vtt'}")

    # JSON
    json_content = generate_json(segments)
    (output_dir / "captions.json").write_text(json_content)
    print(f"Written: {output_dir / 'captions.json'}")

    # Short-form chunks
    chunks = generate_short_form_chunks(segments, args.chunk_duration, args.chunk_chars)
    (output_dir / "short-form-chunks.json").write_text(json.dumps(chunks, indent=2))
    print(f"Written: {output_dir / 'short-form-chunks.json'} ({len(chunks)} chunks)")

    print(f"\nGenerated {len(segments)} caption segments, {len(chunks)} short-form chunks")


if __name__ == "__main__":
    main()
