
# import streamlit as st
# from pytube import YouTube
# import azure.cognitiveservices.speech as speechsdk
# from fpdf import FPDF
# import openai
# from pydub import AudioSegment
# import os


# def transcribe_audio():
#     wav_file = r"F_0101_15y2m_1.wav"
    
#     speech_key = "3a510de7bd2c44deb22d8d8dc984ece7"
#     service_region = "eastus"

#     speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#     audio_config = speechsdk.audio.AudioConfig(filename=wav_file)

#     speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
#     result = speech_recognizer.recognize_once()
    
#     if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#         return result.text
#     else:
#         return None
    

# out = transcribe_audio()
# print(out)


import azure.cognitiveservices.speech as speechsdk

# Set up the Azure Speech configuration
speech_config = speechsdk.SpeechConfig(subscription="3a510de7bd2c44deb22d8d8dc984ece7", region="eastus")

# Set up the audio configuration
audio_file_path = "path_to_your_audio_file.wav"
audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)

# Create a speech recognizer
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

# Perform speech recognition
print("Recognizing speech from audio file...")
result = speech_recognizer.recognize_once_async().get()

# Check the recognition result
if result.reason == speechsdk.ResultReason.RecognizedSpeech:
    print("Recognized: {}".format(result.text))
elif result.reason == speechsdk.ResultReason.NoMatch:
    print("No speech could be recognized.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech Recognition canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))