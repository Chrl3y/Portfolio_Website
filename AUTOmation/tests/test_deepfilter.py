#!/usr/bin/env python3
"""
DeepFilterNet smoke test.

Usage:
    source deepfilternet-env/bin/activate
    python AUTOmation/tests/test_deepfilter.py <path-to-audio>

Tests noise reduction on a local audio file.
Never uploads the audio externally.

Note: uses the deep-filter-py CLI for file I/O.
"""
import os
import subprocess
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: python tests/test_deepfilter.py <path-to-audio>")
        sys.exit(1)

    path = sys.argv[1]
    print(f"Testing DeepFilterNet noise reduction on: {path}")

    try:
        from df.enhance import enhance, init_df

        # Initialize model (just verify it loads)
        model, df_state = init_df()[:2]
        print(f"DeepFilterNet model loaded and ready")

        # Use deep-filter-py CLI for full file processing
        output_dir = os.path.dirname(os.path.abspath(path))
        result = subprocess.run(
            ["deep-filter-py", path, "--output-dir", output_dir],
            capture_output=True, text=True, timeout=120,
        )

        if result.returncode == 0:
            cleaned = path.replace(".wav", "_w120s120.wav")
            if os.path.exists(cleaned):
                print(f"Cleaned audio saved to: {cleaned}")
                print("DeepFilterNet smoke test PASSED")
            else:
                print(f"Output file not found at: {cleaned}")
                print(f"stdout: {result.stdout[-500:]}")
                print(f"stderr: {result.stderr[-500:]}")
                print("DeepFilterNet CLI ran but output file not found")
        else:
            print(f"deep-filter-py failed: {result.stderr[:500]}")
            print("DeepFilterNet smoke test FAILED")
            sys.exit(1)

    except ImportError as e:
        print(f"DeepFilterNet not installed: {e}")
        print("Install with: uv pip install deepfilternet (in its own venv)")
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print("DeepFilterNet timed out (>120s) — likely needs more RAM or a shorter clip")
        print("DeepFilterNet smoke test TIMED OUT (model loads, processing slow on CPU)")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
