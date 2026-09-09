# Voice Tools — AUTOmation

Architecture: preserve Charles' real voice by default.

```
user's actual voice recording
        ↓
audio cleanup (DeepFilterNet)
        ↓
reuse original narration (preferred)
        ↓
optional synthetic voice (only for missing/incorrected sentences)
```

## Installed Tools

| Tool | Status | Notes |
|------|--------|-------|
| faster-whisper | ✅ Installed | CPU mode on M1 Pro, `tiny` model tested |
| WhisperX | ✅ Installed | Requires torch (CPU), alignment + diarization |
| DeepFilterNet | ✅ Installed | Noise reduction, CPU mode works |

## Synthetic Voice Pipeline

- Primary target: **Chatterbox** (Coqui, Apache 2.0) — most practical on M1 Pro
- Secondary: **OpenVoice** (MIT) — voice conversion, lightweight
- Tertiary: **F5-TTS** — if Chatterbox is unreliable

## Constraints

- **ONLY** use Charles' own voice or explicitly consented voices.
- No voice model weights committed to Git.
- Synthetic voice only for:
  - Fixing a missing sentence
  - Correcting a small mistake
  - Optional narration generation
  - User-owned voice cloning experiments

## Scripts

- `AUTOmation/scripts/repair-voice.py` — placeholder for future use
