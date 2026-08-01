import re
from typing import Tuple, List

from modules.memory.database import MemoryDB
from utils.logger import get_logger

logger = get_logger("MemoryCore")

class MemoryCore:
    def __init__(self):
        self.db = MemoryDB()
        logger.info("MemoryCore initialized.")

    def process_command(self, text: str) -> Tuple[str, any]:
        """
        Parses the text and interacts with the database.
        Returns a tuple: (action_type, payload_dict_or_object)
        action_type can be: 'saved', 'found', 'deleted', 'not_found'
        """
        if not text:
            return "not_found", {"query": "", "results": []}

        text_lower = text.lower().strip()

        # 1. Forget / Delete
        if text_lower.startswith("forget") or text_lower.startswith("delete"):
            # Extract what to forget (e.g., "forget about the secret code", "forget my favorite color")
            # Remove the trigger words
            query = re.sub(r'^(forget|delete)(\s+about)?\s+', '', text_lower, flags=re.IGNORECASE).strip()
            if not query:
                return "not_found", {"query": query}
            
            deleted_count = self.db.delete_memory(query)
            if deleted_count > 0:
                return "deleted", {"query": query, "count": deleted_count}
            else:
                return "not_found", {"query": query}

        # 2. Recall / Find
        if text_lower.startswith("recall") or text_lower.startswith("what is") or text_lower.startswith("where is") or text_lower.startswith("who is"):
            # If it's a recall command, find memories matching the query
            query = re.sub(r'^(recall|what is|where is|who is)\s+', '', text_lower, flags=re.IGNORECASE).strip()
            # Remove trailing question marks
            query = query.rstrip('?')
            
            if not query:
                return "not_found", {"query": query}
            
            results = self.db.find_memory(query)
            if results:
                return "found", {"query": query, "results": results}
            else:
                return "not_found", {"query": query}

        # 3. List all
        if "list" in text_lower and "memor" in text_lower:
            results = self.db.get_all_memories()
            if results:
                return "found", {"query": "all memories", "results": results}
            else:
                return "not_found", {"query": "all memories"}

        # 4. Remember / Save (Default fallback or explicit trigger)
        # Typically starts with "remember that" or "remember"
        content_to_save = re.sub(r'^remember(\s+that)?\s+', '', text, flags=re.IGNORECASE).strip()
        
        # If there's content, save it
        if content_to_save:
            added = self.db.add_memory(content_to_save)
            return "saved", {"content": content_to_save}
            
        return "not_found", {"query": text}
