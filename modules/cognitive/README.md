# Cognitive Engine Module

The Cognitive Engine is the intelligence layer of VIRA AI. It receives routed commands that require open-ended knowledge, reasoning, or conversation, and uses Google's Gemini API to generate responses.

## Responsibilities
- Subscribes to `command_routed` events.
- Ignores commands unless their category is "Cognitive".
- Communicates with Google's Gemini API to generate intelligent responses.
- Publishes `cognitive_response` events to the Event Bus.

## Setup
1. Install dependencies:
   ```bash
   pip install google-generativeai python-dotenv
   ```
2. Configure your environment variables in the `.env` file at the root of the project:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   ```

## Event Interface
**Subscribes to:**
- `command_routed`: Triggers when the Command Router classifies speech.

**Publishes:**
- `cognitive_response`: Sent when a valid response is generated. Contains the original prompt and the text response.
- `system_error`: Sent if the Gemini API fails or another internal error occurs.
