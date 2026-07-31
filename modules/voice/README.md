# Voice Module

This module is responsible for continuous listening, wake word detection, and speech-to-text (STT) capabilities for VIRA.

## Dependencies
You need to install the following Python packages:
```bash
pip install SpeechRecognition
pip install pyaudio
```

*(Note: `pyaudio` might require system-level dependencies depending on your OS. For Windows, pip install usually works, but sometimes requires compiling from source or using wheel files).*

## Architecture
- `engine.py`: Interfaces with the Event Bus. Runs an async loop that offloads blocking audio capture to a separate thread to prevent freezing the assistant.
- `core.py`: Uses `SpeechRecognition` to access the microphone. It is completely decoupled from the Event Bus, adhering to our standard.

## Events Published
- `speech_recognized`: payload=`SpeechPayload(text="...", is_wake_word=True/False, confidence=1.0)`
- `system_error`: payload=`{"source": "voice", "error": "..."}`

## Events Subscribed To
- `system_state_changed`: Pauses listening if VIRA goes into a SLEEPING state, saving CPU resources.
