import vosk
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# Load the Vosk model only once to save resources
MODEL_PATH = "vosk-model-small-en-us-0.15"
#MODEL_PATH = "C:\\Users\\marsr\\Documents\\python_class\\PythonCode\\Shrimp Lock\\Github\i2i\\vosk-model-small-en-us-0.15"
model = Model(MODEL_PATH)

# Set up the Vosk model
model = Model("vosk-model-small-en-us-0.15")  # Replace with your model path
recognizer = KaldiRecognizer(model, 16000)

# Record audio from the microphone
def record_audio():
    samplerate = 16000
    duration = 3  # seconds
    print("Recording...")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1)
    sd.wait()
    print("Recording finished.")
    return audio

# Transcribe the audio
def transcribe_audio(audio):
    recognizer.accept_waveform(audio.tobytes())
    result = recognizer.result()
    return result["text"]

# # Main function
# if __name__ == "__main__":
#     audio = record_audio()
#     text = transcribe_audio(audio)
#     print("Transcribed text:", text)

def listen_for_3_seconds():
    audio = record_audio()
    return transcribe_audio(audio)