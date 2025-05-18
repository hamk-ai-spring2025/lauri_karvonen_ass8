import os
import io
import soundfile as sf
import sounddevice as sd
import wavio
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()  # will pick up OPENAI_API_KEY from your env

def generate_audio_response(text: str) -> None:
    """
    Synthesize text via OpenAI TTS and play it directly
    """
    print("Generating audio response...")
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",  # options: alloy, echo, fable, onyx, nova, shimmer
        response_format="mp3",
        input=text,
    )
    
    # Stream into memory buffer
    buffer = io.BytesIO()
    for chunk in response.iter_bytes(chunk_size=4096):
        buffer.write(chunk)
    buffer.seek(0)  # Reset buffer to beginning
    
    # Play audio directly from memory
    play_audio(buffer)
    return None

def play_audio(audio_buffer):
    """
    Play audio from a buffer using sounddevice
    """
    print("Playing audio...")
    with sf.SoundFile(audio_buffer, 'r') as sound_file:
        data = sound_file.read(dtype="float32")
        sd.play(data, sound_file.samplerate)
        sd.wait()  # Wait until playback is finished

def record_audio(seconds: int) -> str:
    """
    Record audio for specified number of seconds
    """
    fs = 44100  # Sample rate
    print("Recording...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished
    print("Recording done")
    
    # Save to file
    output_path = "speech.wav"
    wavio.write(output_path, recording, fs, sampwidth=2)
    return output_path