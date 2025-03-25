import unittest
import os
from text_to_voice import text_to_speech, encode_audio, decode_audio

class TestTextToSpeech(unittest.TestCase):
    
    def test_text_to_speech_and_back(self):
        """Test encoding speech and decoding it back to text."""
        test_text = "Hello, this is a test."

        # Generate speech file
        speech_file = text_to_speech(test_text, "test_output.wav")
        self.assertIsNotNone(speech_file, "TTS failed to generate audio file")
        self.assertTrue(os.path.exists(speech_file), "Output WAV file does not exist")

        # Encode the speech file
        encoded_audio = encode_audio(speech_file)
        self.assertIsNotNone(encoded_audio, "Failed to encode audio file")

        # Decode back to WAV
        decoded_file = decode_audio(encoded_audio, "test_decoded.wav")
        self.assertIsNotNone(decoded_file, "Failed to decode audio file")
        self.assertTrue(os.path.exists(decoded_file), "Decoded WAV file does not exist")

        # Cleanup test files
        os.remove(speech_file)
        os.remove(decoded_file)

if __name__ == "__main__":
    unittest.main()
