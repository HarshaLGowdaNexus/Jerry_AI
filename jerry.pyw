# ==========================================
# REQUIRED PIP INSTALL COMMANDS (Run in terminal):
# pip uninstall google-generativeai -y
# pip install google-genai requests beautifulsoup4 pywhatkit pyautogui pygetwindow SpeechRecognition pyttsx3 pyaudio wikipedia python-dotenv
# ==========================================

import os
import datetime
import time
import requests
import pywhatkit
import pyautogui
import pygetwindow as gw
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import subprocess  
import glob 
import random
from google import genai
from dotenv import load_dotenv

# ------------------------------------------
# JERRY: AI BRAIN SETUP
# ------------------------------------------
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except:
        client = None
else:
    client = None

# ------------------------------------------
# JERRY: CORE ENGINE FUNCTIONS
# ------------------------------------------

def speak(text):
    """Speaks text using Windows SAPI5."""
    print(f"[Jerry]: {text}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id) 
    engine.setProperty('rate', 175) 
    engine.say(text)
    engine.runAndWait()

def listen():
    """Converts voice to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("\n[Jerry is Listening...]")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            print("[Processing...]")
            command = recognizer.recognize_google(audio).lower()
            print(f"[You Said]: {command}")
            return command
        except:
            return ""

# ------------------------------------------
# JERRY: SYSTEM AUTOMATION MODULES
# ------------------------------------------

USER_PROFILE = os.path.expanduser('~')
SEARCH_DIRS = [
    os.path.join(USER_PROFILE, "Desktop"),
    os.path.join(USER_PROFILE, "Documents"),
    os.path.join(USER_PROFILE, "Downloads"),
    os.path.join(USER_PROFILE, "OneDrive", "Desktop"),
    os.path.join(USER_PROFILE, "OneDrive", "Documents"),
]

def smart_search_system(item_name):
    """Deep scans for both FOLDERS and FILES matching the name."""
    speak(f"Scanning Aurora for {item_name}...")
    item_name = item_name.lower()
    
    for directory in SEARCH_DIRS:
        if not os.path.exists(directory): continue
        for root, dirs, files in os.walk(directory):
            # Check Folders
            for d in dirs:
                if item_name in d.lower():
                    target = os.path.join(root, d)
                    subprocess.Popen(f'explorer "{target}"')
                    speak(f"Opened folder {d}")
                    return True
            # Check Files
            for f in files:
                if item_name in f.lower():
                    target = os.path.join(root, f)
                    os.startfile(target)
                    speak(f"Opened file {f}")
                    return True
    return False

def ask_brain(query):
    """AI call with high-speed error handling."""
    if not client:
        speak("AI Brain is offline. Searching web.")
        pywhatkit.search(query)
        return

    try:
        prompt = f"You are Jerry on Aurora Nitro. Answer in 2 sentences: {query}"
        # We use a 5-second timeout to avoid long hangs
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)
        speak(response.text.replace('*', '').replace('#', ''))
    except Exception as e:
        if "429" in str(e):
            speak("AI limit reached. Switching to web search.")
        else:
            speak("Brain error. Checking the web.")
        pywhatkit.search(query)

# ------------------------------------------
# JERRY: MAIN OPERATION LOOP
# ------------------------------------------

def run_jerry():
    print("\n========================================")
    print(" JERRY SYSTEM ONLINE - AURORA NITRO")
    print("========================================")
    speak("Jerry system is online.")

    is_awake = False
    last_wake_time = 0
    WAKE_WINDOW = 30 

    while True:
        command = listen()
        if not command: continue

        current_time = time.time()
        if is_awake and (current_time - last_wake_time > WAKE_WINDOW):
            is_awake = False
            print("[Jerry went to sleep...]")

        if 'jerry' in command or is_awake:
            if 'jerry' in command:
                is_awake = True
                last_wake_time = time.time()
                request = command.replace('hey jerry', '').replace('jerry', '').strip()
                if not request:
                    speak("Yes boss?")
                    continue
            else:
                request = command
                last_wake_time = time.time()

            # --- ROUTING LOGIC ---
            
            if 'exit' in request or 'sleep' in request:
                speak("Goodbye.")
                break

            elif 'time' in request:
                speak(f"The time is {datetime.datetime.now().strftime('%I:%M %p')}")

            elif 'close' in request:
                speak("Closing window.")
                pyautogui.hotkey('alt', 'f4')

            # --- SPECIFIC WEB SHORTCUTS (PRIORITY) ---
            elif 'linkedin' in request:
                speak("Opening LinkedIn.")
                webbrowser.open("https://www.linkedin.com")
            
            elif 'flipkart' in request:
                speak("Opening Flipkart.")
                webbrowser.open("https://www.flipkart.com")

            elif 'amazon' in request:
                speak("Opening Amazon.")
                webbrowser.open("https://www.amazon.in")

            # --- ACADEMIC/UPSC SEARCH (Direct to Web to save quota) ---
            elif any(word in request for word in ['nptel', 'upsc', 'history', 'geography', 'spectrum']):
                speak(f"Searching for {request} on Google.")
                pywhatkit.search(request)

            # --- SYSTEM SEARCH ---
            elif 'open' in request:
                item = request.replace('open', '').replace('the', '').replace('folder', '').replace('file', '').strip()
                
                if 'browser' in item or 'comet' in item:
                    speak("Opening web browser.")
                    webbrowser.open("https://www.google.com")
                elif 'gemini' in item:
                    speak("Opening Gemini.")
                    webbrowser.open("https://gemini.google.com")
                elif smart_search_system(item):
                    pass 
                else:
                    speak(f"Item not found locally. Searching the web for {item}.")
                    pywhatkit.search(item)

            elif 'search' in request or 'google' in request:
                query = request.replace('search', '').replace('for', '').replace('google', '').strip()
                speak(f"Searching Google for {query}.")
                pywhatkit.search(query)

            elif 'play' in request or 'youtube' in request:
                song = request.replace('play', '').replace('youtube', '').strip()
                speak(f"Playing {song} on YouTube.")
                pywhatkit.playonyt(song)

            elif 'pause' in request or 'stop' in request:
                pyautogui.press('playpause')

            else:
                # If it's a multi-word phrase that isn't a command, assume search if quota is tight
                if len(request.split()) > 3:
                    speak("Analyzing request.")
                    ask_brain(request)
                elif request:
                    # If it's a short unrecognized name, just search it
                    speak(f"Searching web for {request}")
                    pywhatkit.search(request)

if __name__ == "__main__":
    run_jerry()