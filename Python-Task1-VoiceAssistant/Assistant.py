import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser


# Text to speech
engine = pyttsx3.init()


def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()



def listen():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")
        r.adjust_for_ambient_noise(source)

        audio = r.listen(source)


    try:
        command = r.recognize_google(audio)

        print("You:", command)

        return command.lower()


    except:

        speak("Sorry, I did not understand")

        return ""




def assistant():

    speak("Hello, I am your voice assistant")


    while True:


        command = listen()



        # Hello
        if "hello" in command:

            speak("Hello, how can I help you")



        # Time
        elif "time" in command:

            current_time = datetime.datetime.now().strftime("%I:%M %p")

            speak(
                "Current time is " + current_time
            )



        # Date
        elif "date" in command or "today" in command:

            current_date = datetime.datetime.now().strftime("%d %B %Y")

            speak(
                "Today's date is " + current_date
            )



        # Open Google
        elif "open google" in command:

            speak("Opening Google")

            webbrowser.open(
                "https://www.google.com"
            )



        # Open YouTube
        elif "open youtube" in command:

            speak("Opening YouTube")

            webbrowser.open(
                "https://www.youtube.com"
            )



        # Search
        elif "search" in command:

            speak("What should I search")

            query = listen()

            webbrowser.open(
                "https://www.google.com/search?q=" + query
            )

            speak("Searching " + query)



        # Exit
        elif "stop" in command or "exit" in command:

            speak("Goodbye")

            break



        else:

            if command != "":

                speak("Please try again")





assistant()