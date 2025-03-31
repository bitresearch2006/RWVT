# test_voice_to_text.py

import os
import wave
import json
import speech_recognition as sr
from voice_to_text import main_program

def test_audio_file_argument(audio_path):
    return os.path.isfile(audio_path)

def test_wav_format_support(audio_path):
    return audio_path.lower().endswith(".wav")

def test_empty_audio_file(audio_path):
    try:
        with wave.open(audio_path, "rb") as wf:
            return wf.getnframes() == 0
    except Exception:
        return False

def test_speech_recognition_output(audio_path):
    return main_program(audio_path)

def run_tests(audio_path):
    result = {"status": "SUCCESS", "message": "", "transcription": ""}
    
    if not test_audio_file_argument(audio_path):
        result["status"] = "ERROR"
        result["message"] = "File not found."
    elif not test_wav_format_support(audio_path):
        result["status"] = "ERROR"
        result["message"] = "Only WAV format is supported."
    elif test_empty_audio_file(audio_path):
        result["status"] = "ERROR"
        result["message"] = "The audio file is empty."
    else:
        response = test_speech_recognition_output(audio_path)
        if response["status"] == "SUCCESS":
            result["transcription"] = response["transcription"]
        else:
            result["status"] = "ERROR"
            result["message"] = response.get("message", "Unknown Error")
    
    print(json.dumps(result, indent=4))

if __name__ == "__main__":
    audio_path = input("Enter path of audio file for testing: ")
    run_tests(audio_path)
