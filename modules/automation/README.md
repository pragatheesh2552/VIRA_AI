# Automation Engine Module

The Automation Engine is responsible for executing safe operating system actions. It listens to routed commands and processes ones that fall under the "Automation" category.

## Responsibilities
- Subscribes to `command_routed` events.
- Ignores commands unless their category is "Automation".
- Uses Python standard libraries (`subprocess`, `os`, `pathlib`, `webbrowser`) to safely open applications, directories, and URLs.
- Gracefully handles missing applications or unknown commands by publishing a failure event instead of crashing the system.

## Supported Features (Version 1)
- **Applications**: notepad, calculator, chrome, edge, vs code
- **Folders**: downloads, documents, desktop
- **Web**: URLs via default browser

## Event Interface
**Subscribes to:**
- `command_routed`: Triggers when the Command Router classifies a voice command as Automation.

**Publishes:**
- `automation_completed`: Sent when an automation task is successfully executed.
- `automation_failed`: Sent when an automation task fails (e.g. app not found, invalid URL).
- `system_error`: Sent on unexpected critical failures.
