import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests

# Weather API Key
API_KEY = "YOUR_API_KEY"

# Text to Speech
engine = pyttsx3.init()

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# Voice Input
def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You:", command)
        return command.lower()

    except:
        speak("Sorry, I didn't understand.")
        return ""

# Weather Function
def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) == "200":
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        speak(f"The temperature in {city} is {temp} degrees Celsius with {desc}")
    else:
        speak("City not found")

# Start Assistant
speak("Voice Assistant Started")

while True:
    command = listen()

    if "hello" in command:
        speak("Hello! How can I help you?")

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%d %B %Y")
        speak(f"Today is {current_date}")

    elif "search" in command:
        speak("What should I search?")
        query = listen()

        if query:
            webbrowser.open(
                f"https://www.google.com/search?q={query}"
            )
            speak(f"Searching for {query}")

    elif "weather" in command:
        speak("Which city?")
        city = listen()

        if city:
            get_weather(city)

    elif "exit" in command:
        speak("Goodbye")
        break