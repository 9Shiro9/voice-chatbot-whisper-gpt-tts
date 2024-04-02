import os
import pyaudio
import pygame
import wave
import keyboard
import time
from dotenv import load_dotenv
from openai import OpenAI

# Function to record audio
def record_audio(output_filename):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

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

    with wave.open(output_filename, "wb") as waveFile:
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))

# Function to get transcription from OpenAI API
def get_transcription(api_key, audio_file_path):
    client = OpenAI(api_key=api_key)
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcription.text

# Function to get response from GPT-3.5 Turbo without conversation history
def get_GPT305_Response(prompt, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role" : "user",
                "content" : "Reply shortly and thoughtfully." +   prompt,
            }
        ],
        response_format={"type" : "text"},
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# Function to get response from GPT-3.5 Turbo with conversation history*
# def get_GPT305_Response(prompt, conversation_history, api_key):
#     client = OpenAI(api_key=api_key)
#     prompt_with_history = "The following is the conversation history.\n" + conversation_history + "\n" + "The following is the current prompt.\n" + prompt + "Give short answers to the current prompt.Also recognize conversation history."
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo-1106",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt_with_history,
#             }
#         ],
#         response_format={"type": "text"},
#         max_tokens=100
#     )
#     return response.choices[0].message.content.strip()


# Function to generate speech from text
def generate_speech_from_text(text, audio_file_path, api_key):
    client = OpenAI(api_key=api_key)
    with client.audio.speech.with_streaming_response.create(
      model="tts-1",
      voice="alloy",
      input=text
    ) as response:
        response.stream_to_file(audio_file_path)

# Function to play audio
def play_audio(audio_file):
    pygame.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()

# Main function
def main():
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    # conversation_history = ""  # Initialize conversation history

    while True:
        output_filename = "recordedFile.wav"
        record_audio(output_filename)
        transcription_text = get_transcription(openai_api_key, output_filename)
        print("You:", transcription_text)
        gpt_response_text = get_GPT305_Response(transcription_text, openai_api_key)
        print("GPT 3.5 Turbo:", gpt_response_text)
        # conversation_history += "'User :" + transcription_text + "." + "\n" + "GPT_response :" + gpt_response_text + ","  # Update conversation history
        speech_file_path = "tts_speech.mp3"
        generate_speech_from_text(gpt_response_text, speech_file_path, openai_api_key)
        play_audio(speech_file_path)

if __name__ == "__main__":
    main()
