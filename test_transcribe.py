import wave
from vosk import Model, KaldiRecognizer

# Initialize Vosk model
model = Model("vosk-model-small-en-us-0.15")
recognizer = KaldiRecognizer(model, 16000)

# Open the recorded file
with wave.open("test_output.wav", "rb") as wf:
    # Ensure the file has the correct sample rate
    assert wf.getframerate() == 16000
    assert wf.getnchannels() == 1

    while True:
        data = wf.readframes(4096)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            print(recognizer.Result())
        else:
            print(recognizer.PartialResult())

    print(recognizer.FinalResult())
