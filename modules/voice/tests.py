import unittest
from unittest.mock import patch, MagicMock
from modules.voice.core import VoiceCore
from modules.voice.models import SpeechPayload

class TestVoiceCore(unittest.TestCase):

    @patch('modules.voice.core.sr.Microphone')
    @patch('modules.voice.core.sr.Recognizer')
    def test_is_wake_word(self, mock_recognizer, mock_microphone):
        # Mocking the initialization to prevent actual hardware access during tests
        mock_recognizer.return_value.adjust_for_ambient_noise = MagicMock()
        core = VoiceCore()
        
        # Test wake word detection logic
        self.assertTrue(core.is_wake_word("hello vira how are you"))
        self.assertTrue(core.is_wake_word("VIRA"))
        self.assertTrue(core.is_wake_word("ok vira tell me a joke"))
        self.assertFalse(core.is_wake_word("hey jarvis"))
        self.assertFalse(core.is_wake_word("what is the weather"))

if __name__ == '__main__':
    unittest.main()
