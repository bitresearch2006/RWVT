import unittest
import base64
import os
from voice_to_text import rwvt

class TestRWVTFunction(unittest.TestCase):
    def setUp(self):
        # Ask user for an audio file path
        file_path = input("Enter the path of the WAV audio file for testing: ")
        
        if not os.path.exists(file_path):
            self.fail(f"File not found: {file_path}")
        
        with open(file_path, "rb") as audio_file:
            self.encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
    
    def test_valid_audio(self):
        sub_json = {"audio": self.encoded_audio}
        response = rwvt(sub_json)
        print("Test Response (Valid Audio):", response)
        self.assertEqual(response["status"], "SUCCESS", f"Expected SUCCESS but got {response}")
        self.assertIn("transcription", response, "Transcription key missing in response")

    def test_invalid_audio(self):
        sub_json = {"audio": "invalid_base64_data"}
        response = rwvt(sub_json)
        print("Test Response (Invalid Audio):", response)
        self.assertEqual(response["status"], "ERROR")
        self.assertIn("error_reason", response)

    def test_empty_audio(self):
        sub_json = {"audio": base64.b64encode(b'').decode("utf-8")}
        response = rwvt(sub_json)
        print("Test Response (Empty Audio):", response)
        self.assertEqual(response["status"], "ERROR")
        self.assertIn("error_reason", response)

if __name__ == "__main__":
    unittest.main()
