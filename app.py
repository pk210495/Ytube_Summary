
import streamlit as st
from pytube import YouTube
import azure.cognitiveservices.speech as speechsdk
from fpdf import FPDF
import openai
from pydub import AudioSegment
import os

# Define functions
def download_audio(youtube_url):
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download(output_path='.')
    return out_file

def convert_audio_to_wav(audio_file):
    sound = AudioSegment.from_file(audio_file)
    wav_file = os.path.splitext(audio_file)[0] + '.wav'
    sound.export(wav_file, format='wav')
    return wav_file

def transcribe_audio(audio_file):
    wav_file = convert_audio_to_wav(audio_file)
    
    speech_key = "8a98ac7ec52c4618bd3d0ebd6529a983"
    service_region = "eastus"

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speechsdk.audio.AudioConfig(filename=wav_file)

    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_recognizer.recognize_once()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    else:
        return None

def summarize_text_with_gpt(text):
    openai.api_key = "insert your key"
    
    response = openai.Completion.create(
        engine="davinci",
        prompt=f"Summarize the following text:\n\n{text}\n\nSummary:",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary

def generate_pdf(summary, output_file="summary.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, summary)
    pdf.output(output_file)

# Streamlit app
def main():
    st.title("YouTube Video Summarizer")

    youtube_url = st.text_input("Enter YouTube URL")
    if st.button("Summarize"):
        with st.spinner('Downloading audio...'):
            audio_file = download_audio(youtube_url)
  
        
        with st.spinner('Transcribing audio...'):
            transcript = transcribe_audio(audio_file)
        
        if transcript:
            with st.spinner('Summarizing text...'):
                summary = summarize_text_with_gpt(transcript)
            
            if summary:
                st.success("Summary generated!")
                st.write(summary)

                generate_pdf(summary)
                st.success("PDF generated!")
                with open("summary.pdf", "rb") as f:
                    st.download_button('Download Summary as PDF', f, file_name='summary.pdf')
            else:
                st.error("Failed to summarize text.")
        else:
            st.error("Failed to transcribe audio.")

if __name__ == "__main__":
    main()
