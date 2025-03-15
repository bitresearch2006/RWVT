import base64
import io
import wave
from gtts import gTTS
import speech_recognition as sr

def execute(sub_json):
    try:
        # Decode the base64-encoded text
        text = sub_json.get("text", "").strip()
        if not text:
            return {"status": "ERROR", "error_reason": "No text provided for conversion."}
        
        # Convert text to speech
        tts = gTTS(text=text, lang='en')
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        
        # Encode the audio to base64
        audio_buffer.seek(0)
        audio_base64 = base64.b64encode(audio_buffer.read()).decode("utf-8")
        
        return {"status": "SUCCESS", "audio": audio_base64}
    
    except Exception as e:
        return {"status": "ERROR", "error_reason": str(e)}
