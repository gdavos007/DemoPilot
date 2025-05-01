import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel

SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024

# Load Whisper model once globally
whisper_model = WhisperModel("base", device="cpu", compute_type="int8")

def listen_and_transcribe_once(duration_sec=7) -> str:
    """
    Records from the mic for `duration_sec` seconds and returns the transcribed text.
    """
    audio_queue = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_queue.put(indata.copy())

    with sd.InputStream(callback=callback, channels=CHANNELS, samplerate=SAMPLE_RATE, blocksize=CHUNK_SIZE):
        print("🎙️ Listening for input...")
        frames = []
        for _ in range(int(SAMPLE_RATE / CHUNK_SIZE * duration_sec)):
            frames.append(audio_queue.get())
        audio_data = np.concatenate(frames, axis=0).flatten()

    segments, _ = whisper_model.transcribe(audio_data, beam_size=1)
    return " ".join([seg.text for seg in segments]).strip()

# Optional: test this file directly
if __name__ == "__main__":
    transcript = listen_and_transcribe_once(duration_sec=5)
    print(f"Transcript: {transcript}")
