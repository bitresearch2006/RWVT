import base64
import io
import wave
import speech_recognition as sr

def execute(sub_json):
    try:
        # Decode the base64-encoded audio
        audio_bytes = base64.b64decode(sub_json["audio"])

        # Create an in-memory buffer for the audio
        audio_buffer = io.BytesIO(audio_bytes)

        # Validate if it's a proper WAV file
        try:
            with wave.open(audio_buffer, "rb") as wav_file:
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                num_channels = wav_file.getnchannels()
                
                # Debugging: Print WAV file properties
                print(f"WAV File Properties: Channels={num_channels}, Sample Width={sample_width}, Frame Rate={frame_rate}")

        except wave.Error as wav_err:
            return {"status": "ERROR", "error_reason": f"Invalid WAV file: {wav_err}"}

        # Reset the buffer position before using it in Speech Recognition
        audio_buffer.seek(0)

        # Process with Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        return {"status": "SUCCESS", "transcription": text}

    except Exception as e:
        return {"status": "ERROR", "error_reason": str(e)}
