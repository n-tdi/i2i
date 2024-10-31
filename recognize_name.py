import pyaudio
import json
import time
from vosk import Model, KaldiRecognizer

# Load the Vosk model only once to save resources
MODEL_PATH = "vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

def listen_for_3_seconds():
    """Listens for audio input for 3 seconds and returns the recognized text."""

    recognizer = KaldiRecognizer(model, 16000)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, 
                    frames_per_buffer=8192, input_device_index=1, input_latency=0.01)

    stream.start_stream()

    print("Listening for 3 seconds...")

    start_time = time.time()
    recognized_text = ""

    try:
        while True:
            # Stop after 3 seconds
            if time.time() - start_time > 3:
                break

            data = stream.read(8192, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                recognized_text = json.loads(result).get("text", "")
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "")
                print(f"Partial: {partial_text}", end="\r")
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    
    stream.stop_stream()
    stream.close()
    audio.terminate()

    print("Finished listening.")
    return recognized_text
