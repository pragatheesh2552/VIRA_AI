# VIRA AI - Standard Module Template

To maintain a scalable and modular Event-Driven Architecture, every feature module in VIRA (Voice, Vision, Automation, Memory, etc.) will follow this strict internal structure. 

This ensures Separation of Concerns (SoC) where the business logic is entirely decoupled from the Event Bus.

## Directory Structure

```text
modules/[module_name]/
├── __init__.py           # Exposes the main Engine/Controller class
├── engine.py             # The integration layer (Interacts with the Event Bus)
├── core.py               # The business logic (Agnostic of the Event Bus)
├── models.py             # Data schemas and Pydantic models
├── exceptions.py         # Module-specific custom errors
└── config.py             # Module-specific configurations and constants
```

## File Purposes

### 1. `__init__.py`
**Purpose:** Makes the directory a Python package and exposes the main class (usually from `engine.py`) so other parts of the application can import it cleanly (e.g., `from modules.voice import VoiceEngine`).

### 2. `engine.py`
**Purpose:** The Integration Layer.
- This is the **only** file in the module that knows about the Core Engine (`EventBus` and `LifecycleManager`).
- It subscribes to relevant system events.
- It translates incoming events into calls to `core.py`.
- It takes the results from `core.py` and publishes them back out as new events.
- *Example:* Listens for `audio_detected` event, passes the audio to `core.py` to transcribe, and then publishes a `text_transcribed` event.

### 3. `core.py` (or `services.py`)
**Purpose:** The Business Logic Layer.
- Does all the actual heavy lifting (e.g., OpenCV logic, PyAutoGUI commands, API requests).
- **Rule:** It must *never* import the `EventBus`. It should just be pure Python functions or classes that take inputs and return outputs.
- This makes the module highly testable in isolation.

### 4. `models.py`
**Purpose:** The Data Layer.
- Defines the data structures used by the module.
- Uses `dataclasses` or `pydantic` schemas for strict type checking.
- *Example:* A `VoiceCommand` model containing `text` and `confidence_score` fields.

### 5. `exceptions.py`
**Purpose:** Error Handling.
- Defines custom exception classes specific to the module.
- *Example:* `CameraNotFoundError`, `MicrophoneMutedError`, `APIConnectionTimeout`. 
- Allows `engine.py` to catch specific errors and publish a `system_error` event safely.

### 6. `config.py`
**Purpose:** Configuration Management.
- Holds local settings, default values, and environment variable loaders specific to this module.
- *Example:* Wake word sensitivity thresholds, API keys, or default camera indexes. 
