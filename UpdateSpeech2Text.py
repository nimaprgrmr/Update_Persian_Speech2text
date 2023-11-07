import speech_recognition as sr
from pydub import AudioSegment
from fastapi import FastAPI, File, UploadFile
import os
from timeit import default_timer as timer
import warnings
warnings.filterwarnings("ignore")


# Initialize the recognizer
recognizer = sr.Recognizer()


# # Define a function to capture a single word of audio
# def capture_word():
#     with sr.Microphone() as source:
#         print("Speak a word...")
#         audio = recognizer.listen(source)
#
#     try:
#         word = recognizer.recognize_google(audio, language="fa-IR")  # Specify Persian (Farsi) language
#         return word
#     except sr.UnknownValueError:
#         print("Speech recognition could not understand audio")
#         return None
#     except sr.RequestError as e:
#         print("Could not request results from Google Web Speech API; {0}".format(e))
#         return None


# Continuously capture words and transcribe them
# command = input("Please type `y` to start the system else type `n`: ").lower()
# while command == 'y':
#     word = capture_word()
#     if word:
#         print("You said:", word)
#     command = input("Please type `y` if you want to continue else type `n`: ").lower()


# FOR CONVERT FILE TO TEXT USE THIS METHOD
# Define the path to your audio file

# audio_file_path = "new_farsi.wav"  # Replace with your actual audio file path
# if audio_file_path.split('.')[-1] != 'wav':
#     # Output WAV file
#     output_wav_file = "new_farsi.wav"
#     # Load the MP3 file
#     audio = AudioSegment.from_mp3(audio_file_path)
#     # Export as WAV
#     audio.export(output_wav_file, format="wav")
# else:
#     output_wav_file = audio_file_path
#
# # Use the AudioFile context manager to open the audio file
# with sr.AudioFile(output_wav_file) as source:
#     audio = recognizer.record(source)
#
# try:
#     transcription = recognizer.recognize_google(audio, language="fa-IR")  # Specify Persian (Farsi) language
#     print("Transcription:", transcription)
# except sr.UnknownValueError:
#     print("Google Web Speech API could not understand audio")
# except sr.RequestError as e:
#     print("Could not request results from Google Web Speech API; {0}".format(e))


app = FastAPI(title="Convert Speech Too Text")


def convert_to_wav(input_file):
    # Load the input audio file using pydub
    audio = AudioSegment.from_file(input_file)

    # Check if the file is not in WAV format
    if audio.channels != 1 or audio.frame_rate != 16000:
        # Convert the audio to WAV format
        audio = audio.set_channels(1).set_frame_rate(16000)

    # Define the output WAV file path
    output_file = "temp_audio.wav"

    # Export the audio to WAV format
    audio.export(output_file, format="wav")

    return output_file


@app.post("/upload")
async def audio_tp_text(audio_file: UploadFile = File(...)):
    start_time = timer()
    with open("temp_audio", "wb") as temp_audio:
        temp_audio.write(audio_file.file.read())

    # Convert the audio to WAV format if needed
    wav_file = convert_to_wav("temp_audio")

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()

    # Load the audio file
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)

    # Use Google Web Speech API to transcribe the audio
    try:
        transcription = recognizer.recognize_google(audio_data, language="fa-IR")
        end_time = timer()
        return {"transcription": transcription, "time": str(round(end_time - start_time)) + " seconds"}
    except sr.UnknownValueError:
        return {"error": "Speech Recognition could not understand the audio"}
    except sr.RequestError:
        return {"error": "Could not request results from Google Speech Recognition"}
    finally:
        # Clean up: Remove temporary files
        os.remove("temp_audio")
        os.remove(wav_file)
