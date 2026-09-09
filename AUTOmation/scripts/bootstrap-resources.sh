#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENDOR_DIR="$ROOT_DIR/vendor"
mkdir -p "$VENDOR_DIR"

clone_if_missing() {
  local url="$1"
  local dest="$2"
  if [ -d "$dest/.git" ]; then
    echo "[skip] $(basename "$dest") already cloned"
  else
    echo "[clone] $url -> $dest"
    git clone --depth 1 "$url" "$dest"
  fi
}

MODE="${1:-core}"

clone_core() {
  clone_if_missing https://github.com/gitroomhq/postiz-app.git "$VENDOR_DIR/postiz-app"
  clone_if_missing https://github.com/n8n-io/n8n.git "$VENDOR_DIR/n8n"
  clone_if_missing https://github.com/activepieces/activepieces.git "$VENDOR_DIR/activepieces"
  clone_if_missing https://github.com/SYSTRAN/faster-whisper.git "$VENDOR_DIR/faster-whisper"
  clone_if_missing https://github.com/m-bain/whisperX.git "$VENDOR_DIR/whisperX"
  clone_if_missing https://github.com/remotion-dev/remotion.git "$VENDOR_DIR/remotion"
  clone_if_missing https://github.com/ManimCommunity/manim.git "$VENDOR_DIR/manim"
  clone_if_missing https://github.com/mermaid-js/mermaid.git "$VENDOR_DIR/mermaid"
}

clone_audio() {
  clone_if_missing https://github.com/openai/whisper.git "$VENDOR_DIR/whisper"
  clone_if_missing https://github.com/Rikorose/DeepFilterNet.git "$VENDOR_DIR/DeepFilterNet"
  clone_if_missing https://github.com/facebookresearch/demucs.git "$VENDOR_DIR/demucs"
}

clone_voice() {
  clone_if_missing https://github.com/myshell-ai/OpenVoice.git "$VENDOR_DIR/OpenVoice"
  clone_if_missing https://github.com/SWivid/F5-TTS.git "$VENDOR_DIR/F5-TTS"
  clone_if_missing https://github.com/coqui-ai/TTS.git "$VENDOR_DIR/TTS"
}

clone_visual_ai() {
  clone_if_missing https://github.com/comfyanonymous/ComfyUI.git "$VENDOR_DIR/ComfyUI"
  clone_if_missing https://github.com/Lightricks/LTX-Video.git "$VENDOR_DIR/LTX-Video"
  clone_if_missing https://github.com/Lightricks/LTX-Desktop.git "$VENDOR_DIR/LTX-Desktop"
}

clone_avatar_optional() {
  clone_if_missing https://github.com/KwaiVGI/LivePortrait.git "$VENDOR_DIR/LivePortrait"
  clone_if_missing https://github.com/TMElyralab/MuseTalk.git "$VENDOR_DIR/MuseTalk"
  clone_if_missing https://github.com/Rudrabha/Wav2Lip.git "$VENDOR_DIR/Wav2Lip"
}

case "$MODE" in
  core) clone_core ;;
  audio) clone_audio ;;
  voice) clone_voice ;;
  visual-ai) clone_visual_ai ;;
  avatar) clone_avatar_optional ;;
  all)
    clone_core
    clone_audio
    clone_voice
    clone_visual_ai
    clone_avatar_optional
    ;;
  *)
    echo "Usage: $0 {core|audio|voice|visual-ai|avatar|all}"
    exit 2
    ;;
esac

echo
cat <<'EOF'
Resources cloned for local experimentation.

Important:
- Do not commit AUTOmation/vendor/ into the portfolio repository.
- Review each code AND model-weight license before production/commercial use.
- Large video models may need CUDA/cloud GPU rather than the local M1 Pro.
- Voice/avatar tools must only be used with user-owned or explicitly consented voices/images.
EOF
