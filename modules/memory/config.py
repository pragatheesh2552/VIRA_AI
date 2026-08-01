import os

# Configuration for the Memory Engine
MEMORY_CONFIG = {
    # We store the DB in a dedicated database folder at the project root
    "db_dir": os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "database"),
    "db_filename": "vira_memory.db"
}
