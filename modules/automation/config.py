import pathlib

# Configuration mapping intent names to Windows executables or URLs
AUTOMATION_CONFIG = {
    "apps": {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "vs code": "code.cmd"
    },
    "folders": {
        "downloads": str(pathlib.Path.home() / "Downloads"),
        "documents": str(pathlib.Path.home() / "Documents"),
        "desktop": str(pathlib.Path.home() / "Desktop")
    }
}
