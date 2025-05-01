# DemoPilot
An AI-powered voice-enabled chatbot assistant for enhancing product demos using Storylane, featuring integration with Carbon Black and Prisma Cloud product knowledge.

## Quick Start

Follow these steps to run the demo:

1. **Install Dependencies**:
   ```bash
   python setup.py
   ```

2. **Add API Keys**:
   - Edit the `.env` file created by the setup script
   - Add your Anthropic API key (required)
   - Add your OpenAI API key (required for LLM responses and optional for Whisper or embeddings)

3. **Run the App**:
   ```bash
   streamlit run storylane_demo_assistant.py
   ```

The app will open in your browser automatically.

## New Features

- **🎤 Real-Time Voice Agent**: Speak to the assistant using your microphone and receive responses verbally and visually
- **🔊 Text-to-Speech Toggle**: Enable or disable spoken responses from the assistant
- **🛑 Stop Speaking Button**: Interrupt the assistant's response playback mid-sentence
- **Storylane Dashboard as Main Visual**: View demo walkthroughs for product features
- **Carbon Black & Prisma Cloud Support**: Ask product-specific questions for each platform
- **Chat + Voice Interface**: Interact via typing or voice with seamless switching
- **Context-Aware Responses**: Answers are enriched based on the active Storylane demo section

## Architecture

This demo showcases the integration of Storylane demos with an AI-powered voice and text-based assistant:

1. **Storylane Integration**: Displays interactive demo walkthroughs
2. **Product Knowledge Agent**: Responds to questions using context + document-based retrieval (RAG)
3. **Real-Time Voice Input**: Captures and transcribes speech using Whisper and Faster-Whisper
4. **Text-to-Speech Output**: Uses pyttsx3 to speak responses aloud
5. **Streamlit UI**: A polished interface combining voice, text, and Storylane visualization

## Key Files

- `storylane_demo_assistant.py` — Streamlit app integrating Storylane + voice assistant
- `realtime_voice_agent.py` — Real-time transcription function (`listen_and_transcribe_once()`)
- `text_to_speech.py` — Handles TTS initialization and speaking logic
- `product_knowledge_agent.py` — Custom RAG-based assistant for product knowledge
- `mock_demo_services.py` — Optional demo section controls
- `setup_script.py` — Installs dependencies and sets up `.env`

## Requirements

- Python 3.8 or higher
- Anthropic API key (Claude model support)
- OpenAI API key (GPT-4o + Whisper)
- Microphone (for voice input)
- Speaker/headset (for voice output)

Install key packages:
```bash
pip install streamlit anthropic openai faster-whisper sounddevice pyttsx3 SpeechRecognition numpy scipy
```

## Troubleshooting

1. Ensure `.env` contains valid keys for Anthropic and OpenAI
2. Install microphone/sound packages: `sounddevice`, `portaudio`, and `pyaudio`
3. If Whisper fails, check CPU compatibility or switch to a smaller model (`tiny`, `base`)
4. On macOS, use `brew install portaudio` to fix sound device errors
5. If no audio plays during TTS, try changing the voice ID in `text_to_speech.py`

## Notes

- The knowledge base is initialized with Carbon Black documentation URLs
- You can customize source documents in `_initialize_with_default_urls()` inside `product_knowledge_agent.py`
- Voice and text interfaces are unified — you can switch between them on the fly

---

**🚀 Demo Tips:**
- Try typing a question like "Is there API access for custom integrations? What methods are used for behavioral analysis and threat detection?"
- Toggle TTS or interrupt responses live for better control during presentations
