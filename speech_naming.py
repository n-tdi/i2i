import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()

def transcribe(timeout, phrase_time_limit):    
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        

    # recognize speech using Sphinx
    try:
        return r.recognize_sphinx(audio)
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
        return None