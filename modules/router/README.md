# Command Router Module

The Command Router is the central nervous system of VIRA's command execution flow. It does **not** execute commands itself; rather, it acts as a high-speed dispatcher.

## Flow
1. Listens for `speech_recognized` events on the central Event Bus.
2. Extracts the recognized text.
3. Uses a rule-based classifier (configured in `config.py`) to determine the target module (`Automation`, `Browser`, `Memory`, `Vision`, `Cognitive`).
4. Publishes a `command_routed` event to the Event Bus containing the classification payload.

## Extending Rules
To add new phrases or modules, simply update the `ROUTER_RULES` dictionary in `config.py`.
