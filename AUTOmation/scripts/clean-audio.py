#!/usr/bin/env python3
"""
Audio cleanup script using DeepFilterNet.

Usage:
    source runtime/deepfilternet-env/bin/activate
    python AUTOmation/scripts/clean-audio.py --input noisy.wav --output clean.wav

Purpose:
    recorded voice --> noise reduction --> clean narration

Uses DeepFilterNet for DNS (Deep Noise Suppression).
All processing is local — no upload.
"""

import argparse
import os
import sys
from pathlib import Path

from deepfilter import DeepFilterNet, InitSchema


def clean_audio(input_path: str, output_path: str, **kwargs) -> str:
    """Run DeepFilterNet noise reduction on an audio file."""
    model = DeepFilterNet(
        model_size=kwargs.get("model_size", "s"),
        enable_amp=True,
    )

    # Process and save
    model.run_inference(
        input_file=input_path,
        output_file=output_path,
        samplerate=kwargs.get("samplerate", 48000),
        n_fft=kwargs.get("n_fft", 1024),
        chunk_nsamples=kwargs.get("chunk_nsamples", 15360),
    )

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Noise reduction for recorded voice using DeepFilterNet."
    )
    parser.add_argument("--input", "-i", required=True, help="Input audio file (wav/mp3/flac)")
    parser.add_argument("--output", "-o", required=True, help="Output cleaned audio file")
    parser.add_argument("--model-size", default="s", choices=["s", "m", "l", "xl"],
                        help="DeepFilterNet model size (default: s for speed)")
    parser.add_argument("--samplerate", type=int, default=48000, help="Output sample rate")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    print(f"[clean-audio] Input:  {args.input}")
    print(f"[clean-audio] Output: {args.output}")
    print(f"[clean-audio] Model:  DeepFilterNet-{args.model_size}")

    clean_audio(args.input, args.output, model_size=args.model_size,
                samplerate=args.samplerate)

    print(f"[clean-audio] Done. Clean audio saved to {args.output}")


if __name__ == "__main__":
    main()
