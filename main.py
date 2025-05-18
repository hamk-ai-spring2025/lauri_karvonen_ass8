from openai import OpenAI
import sounddevice as sd
import os
import keyboard
import threading
import re
from speech import record_audio, transcribe_audio
from chat import ChatBot
from audio import generate_audio_response
from dotenv import load_dotenv
import atexit

load_dotenv()

def cleanup_temp_files():
    for file in os.listdir('.'):
        if file.startswith('speech') and file.endswith('.wav'):
            try:
                os.remove(file)
                print(f"Cleaned up {file}")
            except:
                pass

atexit.register(cleanup_temp_files)

def main():
    """
    Main entry point for the voice chat application.
    Sets up a conversational AI that:
    - Records voice input
    - Transcribes speech to text
    - Generates an AI response
    - Converts that response to speech
    - Monitors for exit commands
    """

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    if not OPENAI_API_KEY:
        print("Please set OPENAI_API_KEY in your .env file.")
        return

    chat_bot = ChatBot()
    print("Voice ChatBot ready! Say 'exit' to quit or press any key to exit.")

    # Flag for keyboard interrupt
    exit_requested = False
    
    def check_for_keypress():
        nonlocal exit_requested
        keyboard.wait()  # Wait for any keypress
        exit_requested = True
        print("\nKeypress detected, exiting after current interaction...")
    
    # Start keyboard listener in separate thread
    keyboard_thread = threading.Thread(target=check_for_keypress)
    keyboard_thread.daemon = True  # Thread will exit when main program exits
    keyboard_thread.start()

    while not exit_requested:
        print("Listening for your voice input...")
        audio_file = record_audio(10)  # 10 seconds recording
        
        # Check if exit was requested during recording
        if exit_requested:
            print("Exiting the chatbot.")
            break
            
        transcription = transcribe_audio(audio_file)
        exit_checker = re.sub(r'[^\w\s]', '', transcription.lower())

        if exit_checker == "exit":
            print("'Exit' command detected. Exiting the chatbot.")
            break

        print(f"You said: {transcription}")
        response = chat_bot.get_response(transcription)
        print(f"ChatBot is responding...")

        # Generate and play audio response
        generate_audio_response(response)

    print("Chat session ended. Goodbye!")

if __name__ == "__main__":
    main()