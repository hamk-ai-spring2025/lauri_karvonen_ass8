# Voice Conversation Chatbot

This project is a voice conversation chatbot that utilizes the ChatGPT API. It allows users to interact with the chatbot using voice prompts, which are transcribed into text. The chatbot maintains conversation history, generates text responses, and converts them to speech. Users can exit the conversation using a keyboard button or by saying the voice command 'exit'.

## Features

- Voice input for user prompts
- Transcription of audio to text using Whisper API
- Conversation history management
- Text-to-speech conversion for responses
- Automatic playback of audio responses
- Exit the conversation via keyboard or voice command

## Project Structure

```
language-trainer
├── __init__.py
├── main.py
├── chat.py
├── speech.py
├── audio.py
└── utils.py
├── .env
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone git clone https://github.com/hamk-ai-spring2025/lauri_karvonen_ass8/
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in the `.env` file:
   ```
   OPENAI_API_KEY=<your_openai_api_key>
   ```

## Usage

To run the chatbot, execute the following command:
```
python main.py
```

Follow the prompts to interact with the chatbot. You can speak your input, and the chatbot will respond with audio playback. 
To end the training session, use the voice prompt 'Exit' to exit the program, or press any key on the keyboard.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
