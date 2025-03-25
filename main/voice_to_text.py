import base64
import io
import wave
import speech_recognition as sr

def encode_audio(file_path):
    """Encodes a given WAV audio file to Base64."""
    try:
        with open(file_path, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
        return encoded_audio
    except Exception as e:
        print(f"Error encoding audio file: {e}")
        return None

def rwvt(sub_json):
    """Decodes Base64 audio, verifies it as a WAV file, and transcribes it to text."""
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
                
                print(f"WAV File Properties: Channels={num_channels}, Sample Width={sample_width}, Frame Rate={frame_rate}")

        except wave.Error as wav_err:
            return {"status": "ERROR", "error_reason": f"Invalid WAV file: {wav_err}"}

        # Reset buffer position for Speech Recognition
        audio_buffer.seek(0)

        # Process with Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_buffer) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                return {"status": "SUCCESS", "transcription": text}
            except sr.UnknownValueError:
                return {"status": "ERROR", "error_reason": "Speech recognition could not understand audio"}
            except sr.RequestError as e:
                return {"status": "ERROR", "error_reason": f"Speech recognition request failed: {e}"}

    except Exception as e:
        return {"status": "ERROR", "error_reason": str(e)}

if __name__ == "__main__":
    file_path = input("Enter the path of the WAV audio file: ")
    encoded_audio = encode_audio(file_path)
    if encoded_audio:
        sub_json = {"audio": encoded_audio}
        result = rwvt(sub_json)
        print("Transcription Result:", result)
