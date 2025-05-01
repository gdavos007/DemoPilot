import pyttsx3
import threading

tts_engine = pyttsx3.init()
tts_thread = None
tts_lock = threading.Lock()

def initialize_tts_engine():
    global tts_engine
    tts_engine.setProperty('rate', 175)
    tts_engine.setProperty('volume', 1.0)
    for voice in tts_engine.getProperty('voices'):
        if 'female' in voice.name.lower() or 'samantha' in voice.id.lower() or 'zira' in voice.id.lower():
            tts_engine.setProperty('voice', voice.id)
            break
    return tts_engine

def _speak_background(text):
    with tts_lock:
        tts_engine.say(text)
        tts_engine.runAndWait()

def speak_text(text):
    global tts_thread
    stop_speaking()  # interrupt any ongoing
    tts_thread = threading.Thread(target=_speak_background, args=(text,))
    tts_thread.start()

def stop_speaking():
    with tts_lock:
        tts_engine.stop()
