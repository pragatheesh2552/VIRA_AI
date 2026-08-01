import urllib.parse
import webbrowser
import re
from typing import Tuple

from modules.browser.config import BROWSER_CONFIG
from modules.browser.exceptions import InvalidURLError
from utils.logger import get_logger

logger = get_logger("BrowserCore")

class BrowserCore:
    def __init__(self):
        logger.info("BrowserCore initialized.")

    def process_command(self, command: str) -> Tuple[str, str]:
        """
        Parses the text and interacts with the webbrowser.
        Returns a tuple: (action_message, opened_url)
        Raises InvalidURLError if the command is unrecognized or url is invalid.
        """
        if not command:
            raise InvalidURLError("Empty command provided.")

        command_lower = command.lower().strip()

        # 1. Web Searches (search google for X, search youtube for Y)
        # Matches: "search google for python", "search youtube python"
        search_match = re.search(r'search\s+(google|youtube)(?:\s+for)?\s+(.+)', command_lower)
        if search_match:
            engine_name = search_match.group(1)
            query = search_match.group(2).strip()
            
            if not query:
                raise InvalidURLError("Search query is empty.")
                
            engine_url_format = BROWSER_CONFIG["search_engines"].get(engine_name)
            if engine_url_format:
                encoded_query = urllib.parse.quote_plus(query)
                final_url = engine_url_format.format(encoded_query)
                logger.info(f"Searching {engine_name} for: '{query}' -> {final_url}")
                webbrowser.open(final_url)
                return f"Searched {engine_name.capitalize()} for '{query}'", final_url

        # 2. Known Sites (open google, open youtube, etc.)
        if command_lower.startswith("open ") or command_lower.startswith("go to "):
            target = re.sub(r'^(open|go to)\s+', '', command_lower).strip()
            
            # Check if it matches a known site
            if target in BROWSER_CONFIG["known_sites"]:
                final_url = BROWSER_CONFIG["known_sites"][target]
                logger.info(f"Opening known site: {target} -> {final_url}")
                webbrowser.open(final_url)
                return f"Opened {target.capitalize()}", final_url
                
            # 3. Direct URLs
            # If not a known site, check if it looks like a valid URL or domain
            # Very basic check: does it contain a dot and no spaces?
            if "." in target and " " not in target:
                final_url = target
                if not final_url.startswith("http://") and not final_url.startswith("https://"):
                    final_url = "https://" + final_url
                
                logger.info(f"Opening URL: {final_url}")
                webbrowser.open(final_url)
                return f"Opened URL", final_url

        # If we reach here, we could not parse a valid browser action
        raise InvalidURLError(f"Could not parse a valid website or search query from: '{command}'")
