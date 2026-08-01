import os
import sqlite3
from typing import List

from modules.memory.config import MEMORY_CONFIG
from modules.memory.exceptions import DatabaseError
from utils.logger import get_logger

logger = get_logger("MemoryDB")

class MemoryDB:
    def __init__(self):
        self.db_dir = MEMORY_CONFIG["db_dir"]
        self.db_path = os.path.join(self.db_dir, MEMORY_CONFIG["db_filename"])
        self._initialize_db()

    def _initialize_db(self):
        """Creates the database directory and the memories table if they don't exist."""
        try:
            os.makedirs(self.db_dir, exist_ok=True)
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # Use UNIQUE on content to prevent duplicate memories easily
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS memories (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL UNIQUE,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
                conn.commit()
            logger.info(f"Database initialized at {self.db_path}")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            raise DatabaseError(f"Initialization failed: {e}")

    def add_memory(self, content: str) -> bool:
        """
        Inserts a new memory into the database. 
        Returns True if added, False if it was a duplicate.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                # INSERT OR IGNORE silently skips if the exact content is already there
                cursor.execute('INSERT OR IGNORE INTO memories (content) VALUES (?)', (content,))
                conn.commit()
                # rowcount is 1 if inserted, 0 if ignored
                if cursor.rowcount > 0:
                    logger.debug(f"Saved memory: {content}")
                    return True
                else:
                    logger.debug(f"Duplicate memory ignored: {content}")
                    return False
        except Exception as e:
            logger.error(f"Failed to add memory: {e}")
            raise DatabaseError(f"Add memory failed: {e}")

    def find_memory(self, query: str) -> List[str]:
        """
        Searches for memories containing the query string (case-insensitive in SQLite LIKE).
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT content FROM memories WHERE content LIKE ? ORDER BY timestamp DESC', (f'%{query}%',))
                results = [row[0] for row in cursor.fetchall()]
                logger.debug(f"Found {len(results)} memories for query: {query}")
                return results
        except Exception as e:
            logger.error(f"Failed to find memory: {e}")
            raise DatabaseError(f"Find memory failed: {e}")

    def delete_memory(self, query: str) -> int:
        """
        Deletes memories containing the query string.
        Returns the number of deleted records.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM memories WHERE content LIKE ?', (f'%{query}%',))
                conn.commit()
                deleted_count = cursor.rowcount
                logger.debug(f"Deleted {deleted_count} memories for query: {query}")
                return deleted_count
        except Exception as e:
            logger.error(f"Failed to delete memory: {e}")
            raise DatabaseError(f"Delete memory failed: {e}")

    def get_all_memories(self) -> List[str]:
        """
        Retrieves all stored memories.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT content FROM memories ORDER BY timestamp DESC')
                results = [row[0] for row in cursor.fetchall()]
                return results
        except Exception as e:
            logger.error(f"Failed to retrieve all memories: {e}")
            raise DatabaseError(f"Get all memories failed: {e}")
