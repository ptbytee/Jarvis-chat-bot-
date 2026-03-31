import sounddevice as sd
import numpy as np
import speech_recognition as sr
import webbrowser
import datetime
import pyttsx3
import wikipedia
import os
import random
from scipy.io.wavfile import write

# -------- INIT SPEECH ENGINE --------
engine = pyttsx3.init()

def speak(text):
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()


# -------- RECORD AUDIO --------
def record_audio(filename="input.wav", duration=5, fs=16000):
    print("🎤 Listening...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()

    recording = (recording * 32767).astype(np.int16)
    write(filename, fs, recording)

    return filename


# -------- SPEECH TO TEXT --------
def recognize_audio(file_path):
    recognizer = sr.Recognizer()

    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print("🗣️ You:", text)
        return text

    except:
        speak("Sorry, I didn't catch that")
        return ""


# -------- COMMAND HANDLER --------
def execute_command(text):

    # -------- WEB --------
    if "youtube" in text:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif "google" in text:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")

    elif "search" in text:
        query = text.replace("search", "").strip()
        speak(f"Searching for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    # -------- TIME / DATE --------
    elif "time" in text:
        now = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {now}")

    elif "date" in text:
        today = datetime.date.today()
        speak(f"Today's date is {today}")

    # -------- WIKIPEDIA --------
    elif "who is" in text or "what is" in text:
        try:
            topic = text.replace("who is", "").replace("what is", "").strip()
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("I couldn't find information")

    # -------- JOKES --------
    elif "joke" in text:
        jokes = [
            "Why did the computer go to therapy? It had too many bugs.",
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why did Python break up with Java? Too many exceptions."
        ]
        speak(random.choice(jokes))

    # -------- MUSIC --------
    elif "play music" in text:
        music_folder = "music"  # change to your folder
        try:
            songs = os.listdir(music_folder)
            os.startfile(os.path.join(music_folder, songs[0]))
            speak("Playing music")
        except:
            speak("Music folder not found")

    # -------- OPEN APPS --------
    elif "open notepad" in text:
        speak("Opening Notepad")
        os.system("notepad")

    elif "open calculator" in text:
        speak("Opening Calculator")
        os.system("calc")

    # -------- SYSTEM INFO --------
    elif "your name" in text:
        speak("I am jarvis, your voice assistant")

    elif "hello" in text or "hi" in text:
        speak("Hello! How can I help you?")

    # -------- EXIT --------
    elif "stop" in text or "exit" in text:
        speak("byeee!")
        return False

    else:
        speak("I don't understand that yet")

    return True


# -------- MAIN LOOP --------
if __name__ == "__main__":
    speak("Voice assistant started")

    while True:
        file = record_audio(duration=4)
        command = recognize_audio(file)

        if command:
            if not execute_command(command):
                break