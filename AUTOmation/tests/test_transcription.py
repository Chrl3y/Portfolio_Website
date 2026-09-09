#!/usr/bin/env python3
"""
faster-whisper smoke test.

Usage:
    source faster-whisper-env/bin/activate
    python AUTOmation/tests/test_transcription.py <path-to-audio-or-video>

Tests transcription on a local audio/video file.
Never uploads the audio externally.
"""
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/test_transcription.py <path-to-audio-or-video>")
        print("Never uploads the audio externally.")
        sys.exit(1)

    path = sys.argv[1]
    print(f"Testing faster-whisper on: {path}")

    try:
        from faster_whisper import WhisperModel

        # Use small model initially
        model = WhisperModel("tiny", device="cpu", compute_type="float32")
        print(f"Model loaded: tiny (CPU mode)")

        # Transcribe
        segments, info = model.transcribe(path)
        print(f"Language: {info.language} (p={info.language_probability:.2f})")
        print(f"Duration: {info.duration:.1f}s")

        print("\n" + "=" * 60)
        print("TRANSCRIPTION RESULT")
        print("=" * 60)
        print(f"Model:       tiny")
        print(f"Language:    {info.language} (p={info.language_probability:.2f})")
        print(f"Duration:    {info.duration:.1f}s")

        seg_list = list(segments)
        print(f"Segments:    {len(seg_list)}")
        print("-" * 60)

        print("SEGMENTS:")
        for seg in seg_list[:10]:
            print(f"  [{seg.start:.2f} -> {seg.end:.2f}] {seg.text}")

        full_text = " ".join(seg.text for seg in seg_list)
        print("-" * 60)
        print("FULL TEXT:")
        print(full_text)
        print("=" * 60)
        print("faster-whisper smoke test PASSED")

    except ImportError as e:
        print(f"faster-whisper not installed: {e}")
        print("Install with: uv pip install faster-whisper (in its own venv)")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
