#!/usr/bin/env python3
"""
faster-whisper smoke test.

Usage:
    source runtime/faster-whisper-env/bin/activate
    python tests/test_transcription.py tests/transcription-test.wav

Tests transcription with the tiny model (CPU mode).
Generates real speech with macOS `say` if no audio file is provided.

Never uploads audio externally.
"""

import sys
import os
import subprocess
from faster_whisper import WhisperModel


def main():
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Auto-generate a speech test file if none provided
        print("No audio file provided. Generating test audio with macOS 'say'...")
        tests_dir = os.path.dirname(os.path.abspath(__file__))
        aiff_path = os.path.join(tests_dir, "transcription-test.aiff")
        wav_path = os.path.join(tests_dir, "transcription-test.wav")

        subprocess.run(
            ["say", "This is the AUTOmation transcription system test for verification.",
             "-o", aiff_path],
            check=True,
        )
        subprocess.run(
            ["ffmpeg", "-y", "-i", aiff_path, "-ar", "16000", "-ac", "1", wav_path],
            check=True,
            capture_output=True,
        )
        audio_path = wav_path
        print(f"Generated: {audio_path}")

    if not os.path.exists(audio_path):
        print(f"ERROR: Audio file not found: {audio_path}")
        sys.exit(1)

    print(f"Transcribing: {audio_path}")
    print("Loading tiny model (CPU)...")

    model = WhisperModel("tiny", device="cpu", compute_type="float32")

    segments, info = model.transcribe(audio_path, beam_size=5)

    for segment in segments:
        print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")

    print(f"\nDetected language: {info.language} "
          f"(probability: {info.language_probability:.2f})")
    print("faster-whisper smoke test PASSED")


if __name__ == "__main__":
    main()
