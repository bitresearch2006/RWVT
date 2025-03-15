import base64

def convert_audio_to_base64(audio_file):
    with open(audio_file, "rb") as file:
        base64_audio = base64.b64encode(file.read()).decode("utf-8")
    return base64_audio

if __name__ == "__main__":
    audio_file_path = "output.wav"  # Change this to your audio file name
    base64_string = convert_audio_to_base64(audio_file_path)
    
    with open("base64_audio.txt", "w") as output_file:
        output_file.write(base64_string)

    print("Base64 conversion completed! Check base64_audio.txt for the encoded string.")
