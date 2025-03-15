import base64
import json
from services.text_to_speech import execute

# Example text input
input_data = {"text": "Hello, Jenifa! This is a text-to-speech conversion test."}

# Execute the function
result = execute(input_data)

# Print the output
if result["status"] == "SUCCESS":
    # Save the base64 audio as an MP3 file
    with open("output.mp3", "wb") as audio_file:
        audio_file.write(base64.b64decode(result["audio"]))
    print("Audio saved as output.mp3. You can play it!")
else:
    print(f"Error: {result['error_reason']}")
