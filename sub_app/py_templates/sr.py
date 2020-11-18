import speech_recognition as sr
def takeCommand(file,lang):
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    harvard = sr.AudioFile(file)
    with harvard as source:
        #r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.record(source)
    try:
    	text=r.recognize_google(audio,language=lang)
    	return text
    except:
    	return None
    

# text=takeCommand('audio_file.wav')
# print(text)