from openai import OpenAI
import sounddevice as sd
import wavio
import os
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
class SpeechHandler:
    def __init__(self):
        self.client = OpenAI()
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def record_audio(self, duration=5, fs=44100):
        print("Recording...")
        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()  # Wait until recording is finished
        print("Recording done")
        wavio.write("speech.wav", myrecording, fs, sampwidth=2)
        return "speech.wav"

    def transcribe_audio(self, audio_file_path):
        print("Transcribing...")
        with open(audio_file_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )
        return transcription.text

    def text_to_speech(self, text):
        response = self.elevenlabs_client.text_to_speech.convert(
            voice_id="pNInz6obpgDQGcFmaJgB",  # Adam pre-made voice
            output_format="mp3_22050_32",
            text=text,
            model_id="eleven_turbo_v2_5",  # use the turbo model for low latency
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        save_file_path = f"{uuid.uuid4()}.mp3"
        with open(save_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)

        print(f"{save_file_path}: A new audio file was saved successfully!")
        return save_file_path

    def play_audio(self, audio_file_path):
        os.system(f"start {audio_file_path}")  # This will play the audio file on Windows

    def handle_voice_command(self):
        audio_file_path = self.record_audio()
        transcription = self.transcribe_audio(audio_file_path)
        print(f"Transcription: {transcription}")
        if transcription.lower() == "exit":
            print("Exiting the conversation.")
            return True
        return False

import os
import sounddevice as sd
import wavio
from openai import OpenAI

def record_audio(seconds: int = 5) -> str:
    """Record `seconds` of audio and write to speech.wav"""
    fs = 44100
    print("Recording...")
    data = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    print("Recording done")
    out_path = "speech.wav"
    wavio.write(out_path, data, fs, sampwidth=2)
    return out_path

def transcribe_audio(audio_file_path: str) -> str:
    """Transcribe the given WAV file via OpenAI Whisper."""
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    with open(audio_file_path, "rb") as f:
        resp = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return resp.text