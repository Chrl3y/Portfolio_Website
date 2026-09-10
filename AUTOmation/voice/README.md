# Voice Tools — AUTOmation

**Policy**: Preserve Charles' real voice by default. Synthetic voice generation is
only used for optional voice repair — fixing a missing sentence, correcting a small
mistake, or replacing a small clip that cannot be re-recorded.

## Architecture

```
user's actual voice recording
        ↓
audio cleanup (prepare-audio.sh → DeepFilterNet optional)
        ↓
reuse original narration (preferred)

IF a small clip needs replacement:
voice repair tool (synthetic) → splice into narration
        ↓
ffmpeg assemble final narration
```

## Voice Repair Candidates (NOT YET INSTALLED)

The following tools were surveyed but have NOT been installed, tested, or selected:

### Chatterbox
- **Status**: Candidate only
- **License**: MIT (open source)
- **Local**: Yes (PyTorch-based)
- **Apple Silicon**: Untested — requires local verification
- **Quality**: Unknown for this use case

### OpenVoice
- **Status**: Candidate only
- **License**: MIT (open source)
- **Local**: Yes
- **Apple Silicon**: Untested
- **Quality**: Unknown

### F5-TTS
- **Status**: Candidate only
- **License**: MIT (open source)
- **Local**: Yes
- **Apple Silicon**: Untested
- **Quality**: Unknown

### Edge TTS
- **Status**: System default provider
- **License**: Free tier available
- **Local**: No (requires network)
- **Quality**: Decent for simple clips

## Decision Criteria for Selection

A voice repair tool will be selected based on:

1. **Runs on Apple Silicon (M1 Pro)** without GPU
2. **No external API dependency** (works offline)
3. **Voice quality** matches the user's speaking style closely enough for seamless splicing
4. **License** permits local use in a personal portfolio project

## Next Steps

Before selecting a voice repair tool:

1. Install Chatterbox locally and run a quality comparison
2. Measure CPU/RAM usage on Apple Silicon
3. Verify voice similarity against a sample of the user's actual voice
4. Test seamless splicing with FFmpeg

## Voice Repair Script (Placeholder)

`AUTOmation/scripts/repair-voice.py` — this file exists but does NOT implement
synthetic voice generation yet. It will only be connected to a verified tool.
