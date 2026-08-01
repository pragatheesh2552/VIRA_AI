import os
from mss import mss
from PIL import Image

from modules.vision.config import VISION_CONFIG
from modules.vision.exceptions import ScreenshotError
from utils.logger import get_logger

logger = get_logger("ScreenCapture")

class ScreenCapture:
    def __init__(self):
        self.temp_path = VISION_CONFIG["temp_screenshot_path"]
        
        # Ensure the temp directory exists
        os.makedirs(os.path.dirname(self.temp_path), exist_ok=True)
        logger.info("ScreenCapture initialized.")

    def capture(self) -> Image.Image:
        """
        Takes a screenshot of the primary monitor.
        Returns a PIL Image object.
        """
        try:
            with mss() as sct:
                # Capture the primary monitor
                monitor = sct.monitors[1]
                sct_img = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                logger.debug("Successfully captured screen.")
                return img
        except Exception as e:
            logger.error(f"Failed to capture screen: {e}")
            raise ScreenshotError(f"Screen capture failed: {e}")
