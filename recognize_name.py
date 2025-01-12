import sounddevice
import json
import time
from vosk import Model, KaldiRecognizer
import vosk

# Load the Vosk model only once to save resources
MODEL_PATH = "vosk-model-small-en-us-0.15"
MODEL_PATH = "C:\\Users\\marsr\\Documents\\python_class\\PythonCode\\Shrimp Lock\\Github\i2i\\vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

def listen_for_3_seconds():
    """Listens for audio input for 3 seconds and returns the recognized text."""

    recognizer = KaldiRecognizer(model, 16000)

    audio = sounddevice.RawInputStream()
    audio.start()

    print("Listening for 3 seconds...")

    start_time = time.time()
    recognized_text = ""

    try:
        while True:
            # Stop after 3 seconds
            if time.time() - start_time > 3:
                break

            data = audio.read(audio.read_available)
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                recognized_text = json.loads(result).get("text", "")
            else:
                partial_result = recognizer.PartialResult()
                partial_text = json.loads(partial_result).get("partial", "")
                print(f"Partial: {partial_text}", end="\r")

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    
    audio.close()

    print("Finished listening. " + recognized_text)
    return recognized_text

#print(listen_for_3_seconds())

#model = vosk.Model(MODEL_PATH) 

def callback(indata, frames, time, status):
    if status:
        #print(status, file=sys.stderr)
        pass
    recognizer = vosk.KaldiRecognizer(model, 16000)
    if recognizer.AcceptWaveform(indata):
        print(recognizer.Result())

with sounddevice.RawInputStream(samplerate=16000, channels=1, dtype='int16', callback=callback):
    while True:
        sounddevice.sleep(100)