import os
import subprocess
import webbrowser
import pathlib
import re
from modules.automation.config import AUTOMATION_CONFIG
from modules.automation.exceptions import ActionFailedError
from utils.logger import get_logger

logger = get_logger("AutomationCore")

class AutomationCore:
    def __init__(self):
        logger.info("AutomationCore initialized.")

    def execute_command(self, command: str) -> str:
        """
        Parses the command and executes the corresponding OS action.
        Returns a success message, or raises ActionFailedError on failure.
        """
        if not command:
            raise ActionFailedError("Empty command provided.")
            
        command_lower = command.lower().strip()
        
        # 1. Check for Web URLs
        # Basic regex to catch "open google.com", "go to https://example.com"
        url_match = re.search(r'(?:open|go to) (https?://\S+|\S+\.\w{2,})', command_lower)
        if url_match:
            url = url_match.group(1)
            if not url.startswith('http'):
                url = 'https://' + url
            logger.info(f"Opening URL: {url}")
            webbrowser.open(url)
            return f"Opened website: {url}"

        # 2. Check for Folders
        if "open" in command_lower:
            for folder_name, folder_path in AUTOMATION_CONFIG["folders"].items():
                if folder_name in command_lower:
                    try:
                        # Validate path exists
                        if not os.path.exists(folder_path):
                            raise ActionFailedError(f"Folder not found: {folder_path}")
                        
                        logger.info(f"Opening folder: {folder_path}")
                        os.startfile(folder_path)
                        return f"Opened folder: {folder_name}"
                    except Exception as e:
                        logger.error(f"Failed to open folder {folder_name}: {e}")
                        raise ActionFailedError(f"Could not open folder {folder_name}: {e}")

        # 3. Check for Applications
        if "open" in command_lower or "launch" in command_lower or "start" in command_lower:
            for app_name, executable in AUTOMATION_CONFIG["apps"].items():
                if app_name in command_lower:
                    try:
                        logger.info(f"Launching application: {app_name} ({executable})")
                        # Use subprocess.Popen so we don't block
                        # shell=True is sometimes needed for things like code.cmd or if path is not absolute but in PATH
                        subprocess.Popen(executable, shell=True)
                        return f"Opened application: {app_name}"
                    except Exception as e:
                        logger.error(f"Failed to open application {app_name}: {e}")
                        raise ActionFailedError(f"Could not open {app_name}. It might not be installed or in PATH.")
                        
        # If we reached here, we couldn't match the command
        raise ActionFailedError(f"Action not recognized or supported for command: '{command}'")
