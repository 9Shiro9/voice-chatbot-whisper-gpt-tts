import os
import pygame
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=openai_api_key)

speech_file_path = Path(__file__).parent / "tts_speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input="Today is a wonderful day to build something people love!"
)

response.stream_to_file(speech_file_path)

def play_audio(audio_file):
    # Initialize pygame
    pygame.init()

    # Load the audio file
    pygame.mixer.music.load(audio_file)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Quit pygame
    pygame.quit()

if __name__ == "__main__":
    audio_file = "tts_speech.mp3"  # Replace this with the path to your audio file
    play_audio(audio_file)
