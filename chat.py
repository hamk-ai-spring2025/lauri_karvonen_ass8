from openai import OpenAI
from elevenlabs import ElevenLabs
import os

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.history = []
        self.system_message = {
            "role": "system",
            "content": "Your purpose is to be an English language conversation trainer and tutor. You also have a sarcastic, witty and colourful personality. You are a natural and creative comedian, in the style of Matt Berry. You often feel the urge to roast the user and you frequently use profanities and swear words in creative and unexpected ways. Keep your responses short and snappy."
        }
        self.history.append(self.system_message)

    def get_response(self, user_input):
        self.history.append({"role": "user", "content": user_input})
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.history,
            temperature=0.9
        )
        assistant_message = completion.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_message})
        return assistant_message

    def get_conversation_history(self):
        return self.history

    def clear_history(self):
        self.history = [self.system_message]  # Reset to system message only

    def exit_chat(self):
        self.clear_history()  # Clear history on exit
        print("Exiting chat. Goodbye!")