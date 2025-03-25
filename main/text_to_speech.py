import base64
import io
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text):
    """Convert text to speech and return Base64 encoded audio."""
    try:
        tts = gTTS(text=text, lang="en")
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Convert MP3 to WAV for consistency
        audio = AudioSegment.from_file(audio_buffer, format="mp3")
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        
        # Encode WAV file to Base64
        encoded_audio = base64.b64encode(wav_buffer.getvalue()).decode("utf-8")
        return encoded_audio
    except Exception as e:
        print(f"Error in TTS: {e}")
        return None

def decode_and_play_audio(encoded_audio):
    """Decode Base64 encoded audio and play it."""
    try:
        audio_bytes = base64.b64decode(encoded_audio)
        audio_buffer = io.BytesIO(audio_bytes)
        
        # Load and play audio
        audio = AudioSegment.from_file(audio_buffer, format="wav")
        play(audio)
    except Exception as e:
        print(f"Error playing audio: {e}")

if __name__ == "__main__":
    text = input("Enter the text to convert to speech: ").strip()
    encoded_audio = text_to_speech(text)
    
    if encoded_audio:
        print("\n🔹 Base64 Encoded Audio:", encoded_audio[:100] + "...")  # Print only first 100 chars
        print("\n▶ Playing audio now...\n")
        decode_and_play_audio(encoded_audio)
