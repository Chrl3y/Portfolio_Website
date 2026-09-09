#!/usr/bin/env python3
"""
WhisperX smoke test.

Usage:
    source runtime/whisperx-env/bin/activate
    python AUTOmation/tests/test_whisperx.py <path-to-audio-or-video>

Tests WhisperX alignment + diarization on a local audio file.
Never uploads the audio externally.
"""
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/test_whisperx.py <path-to-audio-or-video>")
        print("Never uploads the audio externally.")
        sys.exit(1)

    path = sys.argv[1]
    print(f"Testing WhisperX on: {path}")
    print("NOTE: WhisperX requires torch. If this fails on CPU, use faster-whisper instead.")
    print()

    try:
        import whisperx
        print("WhisperX imported successfully")

        # Use small model for smoke test
        model = whisperx.load_model("tiny", "cpu")
        print("Model loaded: tiny")

        # Transcribe
        result = model.transcribe(path)
        print("Transcription complete!")
        print(f"Segments: {len(result['segments'])}")
        for seg in result["segments"][:5]:
            print(f"  [{seg['start']:.2f} -> {seg['end']:.2f}] {seg['text']}")

    except ImportError as e:
        print(f"WhisperX not installed: {e}")
        print("Install with: uv pip install whisperx (in its own venv)")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
