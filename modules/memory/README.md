# Memory Engine Module

The Memory Engine provides persistent storage capabilities for VIRA AI, enabling it to remember and recall information across sessions.

## Responsibilities
- Subscribes to `command_routed` events.
- Processes commands categorized as "Memory".
- Uses a local `sqlite3` database to store strings persistently.
- Performs intent parsing to detect if the user wants to remember, recall, forget, or list memories.
- Automatically handles duplicate entries by ignoring exact duplicates.

## Features (Version 1)
- **Remember**: Saves a piece of information (e.g. "remember my favorite color is blue").
- **Recall**: Fetches information containing a keyword (e.g. "recall favorite color").
- **Forget**: Deletes information matching a keyword (e.g. "forget favorite color").
- **List**: Lists all stored memories.

## Event Interface
**Subscribes to:**
- `command_routed`: Triggers when the Command Router classifies a voice command as Memory.

**Publishes:**
- `memory_saved`: Fired when a new memory is successfully inserted into the DB.
- `memory_found`: Fired when a recall or list query finds results.
- `memory_deleted`: Fired when memories matching a query are removed.
- `memory_not_found`: Fired when a query yields no results, or nothing is deleted.
