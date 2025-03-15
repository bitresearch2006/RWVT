import requests
import json
import re
import pyttsx3
import base64

SERVER_URL = "http://127.0.0.1:5000/web_server"
MAX_TEXT_LENGTH = 5000  # Max limit for text input

# Function to clean and validate input text
def validate_text(text):
    if not text or text.strip() == "":
        print("\n[Error] Input text cannot be empty.")
        exit()
    if re.search(r'[^\x00-\x7F]', text):  # Check for non-ASCII characters
        print("\n[Error] Input contains unsupported characters. Please enter valid text.")
        exit()
    if len(text) > MAX_TEXT_LENGTH:
        print(f"\n[Error] Input text is too long. Maximum allowed length is {MAX_TEXT_LENGTH} characters.")
        exit()
    return text

# Function to encode audio file as base64
def encode_audio(file_path):
    try:
        with open(file_path, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode("utf-8")
            return encoded_audio  # Ensure proper encoding
    except Exception as e:
        print(f"\n[Error] Failed to encode audio file: {e}")
        exit()


# Function to send request to server
def send_request(request_id, service_name, sub_json, request_type):
    payload = {
        "Request_ID": request_id,
        "Service_Name": service_name,
        "Sub_JSON": sub_json,
        "Request_Type": request_type
    }

    print("\n[Client] Sending Request to Server...")
    print(json.dumps(payload, indent=4))

    try:
        response = requests.post(SERVER_URL, json=payload)
        if response.status_code == 200:
            response_json = response.json()
            print("\n[Server Response]:", json.dumps(response_json, indent=4))
            
            if service_name == "text_to_speech":
                if response_json.get("status") == "SUCCESS":
                    print("\nPlaying generated speech...")
                    engine = pyttsx3.init()
                    engine.say(sub_json["text"])
                    engine.runAndWait()
                else:
                    print("\n[Error] Text-to-Speech conversion failed.")

        else:
            print(f"\n[Error] Received status code: {response.status_code}")
    except Exception as e:
        print(f"\n[Error] Request failed: {e}")

if __name__ == "__main__":
    request_id = input("Enter Request ID: ").strip()
    service_name = input("Enter Service Name (voice_to_text / text_to_speech): ").strip()
    request_type = input("Enter Request Type (INLINE / FUTURE_CALL): ").strip().upper()
    
    sub_json = {}

    if service_name == "text_to_speech":
        text_input = input("Enter Text for Speech Conversion: ").strip()
        text_input = validate_text(text_input)
        sub_json = {"text": text_input}
    
    elif service_name == "voice_to_text":
        file_path = input("Enter Path to Audio File (WAV format): ").strip()
        audio_base64 = encode_audio(file_path)
        sub_json = {"audio": audio_base64}
    
    else:
        print("\n[Error] Invalid Service Name!")
        exit()
    
    send_request(request_id, service_name, sub_json, request_type)