# voice_to_text.py (Main Program)

import base64
import wave
import speech_recognition as sr

def main_program(audio_path):
    try:
        # Encode audio to base64
        with open(audio_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')

        # Check WAV format
        if not audio_path.lower().endswith(".wav"):
            return {"status": "ERROR", "message": "Unsupported audio format. Only WAV supported."}

        # Get audio properties
        with wave.open(audio_path, 'rb') as wav_file:
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            frame_rate = wav_file.getframerate()
        print(f"WAV File: Channels={channels}, Sample Width={sample_width}, Frame Rate={frame_rate}")

        # Recognize Speech
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        transcription = recognizer.recognize_google(audio_data)

        return {"status": "SUCCESS", "transcription": transcription}

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}
