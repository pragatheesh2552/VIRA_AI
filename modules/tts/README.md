# TTS Engine Module

The Text-To-Speech Engine listens for successful operations and errors from other modules and speaks responses aloud to the user using the `pyttsx3` library (offline speech).

## Responsibilities
- Provide a vocal interface for VIRA AI's actions.
- Maintain a thread-safe Queue to ensure phrases do not overlap and do not block the asynchronous Event Bus.
- Automatically format payloads from various events into naturally spoken phrases.

## Subscribed Events
- `cognitive_response`
- `automation_completed` & `automation_failed`
- `browser_completed` & `browser_failed`
- `memory_saved`, `memory_found`, `memory_deleted`, `memory_not_found`

## Architecture Notes
Because `pyttsx3.runAndWait()` is a blocking, thread-sensitive call (specifically on Windows COM), `TTSCore` spawns a dedicated daemon thread on initialization. The Event Bus callbacks in `TTSEngine` push phrases to a thread-safe Queue which the background thread continuously processes.
