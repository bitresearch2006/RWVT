import base64
import io
import wave
import speech_recognition as sr
import logging
import time

def rwvt(sub_json, diagnostics=False):
    """Decodes Base64 audio, verifies it as a WAV file, and transcribes it to text."""
    if diagnostics:
        logging.basicConfig(filename='rwvt_log.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    
    def log_event(message, error_message=None):
        if diagnostics:
            if error_message:
                logging.error(f"{message} - Error: {error_message}")
            else:
                logging.info(message)
    
    start_time = time.time()
    try:
        log_event("Starting rwvt function")
        
        # Decode the base64-encoded audio
        audio_bytes = base64.b64decode(sub_json["audio"])
        log_event("Decoded base64 audio")

        # Create an in-memory buffer for the audio
        audio_buffer = io.BytesIO(audio_bytes)
        log_event("Created in-memory buffer for audio")

        # Validate if it's a proper WAV file
        try:
            with wave.open(audio_buffer, "rb") as wav_file:
                sample_width = wav_file.getsampwidth()
                frame_rate = wav_file.getframerate()
                num_channels = wav_file.getnchannels()
                
                log_event(f"WAV File Properties: Channels={num_channels}, Sample Width={sample_width}, Frame Rate={frame_rate}")
                print(f"WAV File Properties: Channels={num_channels}, Sample Width={sample_width}, Frame Rate={frame_rate}")

        except wave.Error as wav_err:
            log_event("Invalid WAV file", error_message=str(wav_err))
            return {"status": "ERROR", "error_reason": f"Invalid WAV file: {wav_err}"}

        # Reset buffer position for Speech Recognition
        audio_buffer.seek(0)
        log_event("Reset buffer position for speech recognition")

        # Process with Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_buffer) as source:
            audio_data = recognizer.record(source)
            log_event("Recorded audio data for speech recognition")
            try:
                text = recognizer.recognize_google(audio_data)
                log_event("Speech recognition successful")
                return {"status": "SUCCESS", "transcription": text}
            except sr.UnknownValueError:
                log_event("Speech recognition could not understand audio", error_message="UnknownValueError")
                return {"status": "ERROR", "error_reason": "Speech recognition could not understand audio"}
            except sr.RequestError as e:
                log_event("Speech recognition request failed", error_message=str(e))
                return {"status": "ERROR", "error_reason": f"Speech recognition request failed: {e}"}

    except Exception as e:
        log_event("Exception occurred", error_message=str(e))
        return {"status": "ERROR", "error_reason": str(e)}
    finally:
        end_time = time.time()
        duration = end_time - start_time
        log_event(f"rwvt function completed in {duration:.2f} seconds")

