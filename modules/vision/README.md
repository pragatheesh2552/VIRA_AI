# Vision Engine Module

The Vision Engine provides multimodal visual understanding capabilities to VIRA AI. It is capable of capturing the user's screen in real-time and utilizing the Gemini API to analyze the visual content.

## Responsibilities
- Subscribes to `command_routed` events (category: "Vision").
- Uses `mss` for extremely fast, cross-platform screen captures.
- Uses `Pillow` (PIL) to handle image data.
- Leverages the exact same robust **Dynamic Model Fallback** strategy as the Cognitive Engine to avoid crashes caused by deprecated models.
- Uploads the captured screen alongside the user's prompt (e.g. "what is on my screen?") to Gemini.

## Features (Version 1)
- **Screen Capture**: Takes a screenshot of the primary monitor instantly.
- **Visual Q&A**: Answers questions about the current state of the user's screen.
- **Text Recognition**: Can read visible text from the screen if asked.

## Event Interface
**Subscribes to:**
- `command_routed`: Triggers when the Command Router classifies a voice command as a Vision intent.

**Publishes:**
- `vision_response`: Fired when Gemini successfully processes the image and returns a textual description or answer.
- `vision_failed`: Fired when `mss` fails to capture the screen, or all Gemini models fail to process the image due to rate limits or deprecation.
