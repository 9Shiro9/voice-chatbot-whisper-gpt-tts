import pyaudio
import wave
import keyboard
import time

FORMAT = pyaudio.paInt16
CHANNELS = 1.
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