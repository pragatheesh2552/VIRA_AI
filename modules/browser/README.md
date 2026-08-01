# Browser Engine Module

The Browser Engine handles opening websites, navigating to direct URLs, and performing web searches using the system's default browser.

## Responsibilities
- Subscribes to `command_routed` events (category: "Browser").
- Uses the standard `webbrowser` Python module.
- Safely encodes search queries using `urllib.parse`.
- Handles unknown or invalid URLs by publishing failure events instead of throwing exceptions.

## Features (Version 1)
- **Known Sites**: Open popular sites directly (e.g. "open google", "open youtube", "open github", "open chatgpt", "open gmail").
- **Web Search**: Perform searches automatically (e.g. "search google for python programming", "search youtube for funny cats").
- **Direct URLs**: Open specific domains (e.g. "open wikipedia.org", "open https://example.com").

## Event Interface
**Subscribes to:**
- `command_routed`: Triggers when the Command Router classifies a voice command as a Browser intent.

**Publishes:**
- `browser_completed`: Fired when a URL or search query is successfully sent to the browser.
- `browser_failed`: Fired when the command text doesn't contain a valid site, URL, or recognized search intent.
