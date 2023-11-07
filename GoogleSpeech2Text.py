import speech_recognition as sr
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile
import os
from timeit import default_timer as timer
import warnings
warnings.filterwarnings("ignore")


# Initialize the recognizer
recognizer = sr.Recognizer()


# Define a function to capture a single word of audio
def capture_word():
    with sr.Microphone() as source:
        print("Speak a word...")
        audio = recognizer.listen(source)

    try:
        word = recognizer.recognize_google(audio, language="fa-IR")  # Specify Persian (Farsi) language
        return word
    except sr.UnknownValueError:
        print("Speech recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Web Speech API; {0}".format(e))
        return None


# # Continuously capture words and transcribe them
# command = input("Please type `y` to start the system else type `n`: ").lower()
# while command == 'y':
#     word = capture_word()
#     if word:
#         print("You said:", word)
#     command = input("Please type `y` if you want to continue else type `n`: ").lower()


# FOR CONVERT FILE TO TEXT USE THIS METHOD

# Define the path to your audio file
audio_file_path = "new_farsi.wav"  # Replace with your actual audio file path
if audio_file_path.split('.')[-1] != 'wav':
    # Output WAV file
    output_wav_file = "new_farsi.wav"
    # Load the MP3 file
    audio = AudioSegment.from_mp3(audio_file_path)
    # Export as WAV
    audio.export(output_wav_file, format="wav")
else:
    output_wav_file = audio_file_path

# Use the AudioFile context manager to open the audio file
with sr.AudioFile(output_wav_file) as source:
    audio = recognizer.record(source)

try:
    transcription = recognizer.recognize_google(audio, language="fa-IR")  # Specify Persian (Farsi) language
    print("Transcription:", transcription)
except sr.UnknownValueError:
    print("Google Web Speech API could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Web Speech API; {0}".format(e))