import os
import pyaudio
import pygame
import wave
import keyboard
import time
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "recordedFile.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT , channels=CHANNELS , rate=RATE, input=True, frames_per_buffer=CHUNK)

frames = []
print("Press space to start recording.")
keyboard.wait("space")
print("Recording ... Press SPACE to stop.")
time.sleep(0.2)

while True:
    try:
        data = stream.read(CHUNK)
        frames.append(data)
    except KeyboardInterrupt:
        break
    if keyboard.is_pressed('space'):
        print("Stopping recording after a brief delay ...")
        time.sleep(0.2)
        break

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(OUTPUT_FILENAME , "wb")
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Construct the absolute path to the MP3 file
mp3_file_path = os.path.join(os.path.dirname(__file__), "recordedFile.wav")

# Open the MP3 file in binary mode
with open(mp3_file_path, "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )

# Print the transcription text
print( "You : " + transcription.text)

def get_GPT305_Response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role" : "user",
                "content" : prompt,
            }
        ],
        response_format={"type" : "text"},
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

gpt_response_text = get_GPT305_Response(transcription.text)
print("GPT 3.5 Turbo : " + gpt_response_text)

speech_file_path = Path(__file__).parent / "tts_speech.mp3"
with client.audio.speech.with_streaming_response.create(
  model="tts-1",
  voice="onyx",
  input=gpt_response_text
) as response:
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
