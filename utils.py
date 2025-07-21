import speech_recognition as sr

# List all available microphone devices, helpful if multiple mics are attached
print("Available microphones:")
for idx, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"{idx}: {name}")

# ------- Select your mic here (default: first working mic) --------
# Set your desired mic index (default is 0 if you are not sure)
MIC_INDEX = 0

try:
    mic = sr.Microphone(device_index=MIC_INDEX)
except OSError:
    print("Mic NOT found or unavailable! Check connection and drivers.")
    exit()

r = sr.Recognizer()

with mic as source:
    print("Adjusting for ambient noise... Please remain silent.")
    r.adjust_for_ambient_noise(source, duration=1)  # helps with noisy background

    print("Say something!")
    audio = r.listen(source)

try:
    # Recognize using Google Web Speech API (default, requires Internet)
    text = r.recognize_google(audio, language='en-IN')  # choose 'en-IN' for Hindi English, 'en-US' for US English
    print("You said:", text)
except sr.UnknownValueError:
    print("Sorry, couldn't understand your speech.")
except sr.RequestError as e:
    print("Could not request results; check your Internet connection.", e)
