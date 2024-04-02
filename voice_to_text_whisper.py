import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Construct the absolute path to the MP3 file
mp3_file_path = os.path.join(os.path.dirname(__file__), "how_are_you.wav")

# Open the MP3 file in binary mode
with open(mp3_file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

# Print the transcription text
print(transcription.text)
