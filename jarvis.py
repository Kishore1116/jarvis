import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipediaapi
import requests
import time

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to make Jarvis speak
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio)
            print(f"User said: {query}\n")
        except Exception as e:
            print("Could not understand your command, please try again.")
            speak("Could not understand your command, please try again.")
            return None
        return query.lower()

# Function to search Wikipedia
def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(query)
    
    if page.exists():
        speak(f"Here is what I found on {query}")
        print(page.summary[:500])
        speak(page.summary[:500])
    else:
        speak("Sorry, I couldn't find any information on that topic.")

# Function to get weather information
def get_weather(city):
    api_key = "1536fffec7aa626142d0ca8374295739"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(base_url)
    
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        speak(f"The temperature in {city} is {temperature} degrees Celsius with {description}.")
    else:
        speak("Sorry, I couldn't retrieve the weather information.")

# Main logic for Jarvis
def jarvis():
    speak("Hello, I am Jarvis. How can I assist you today?")
    
    while True:
        query = take_command()

        if query is None:
            continue

        # Commands for specific tasks
        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            search_wikipedia(query.strip())
        
        elif 'open google' in query:
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")
        
        elif 'weather in' in query:
            city = query.split("in")[-1].strip()
            speak(f"Getting weather information for {city}.")
            get_weather(city)

        elif 'stop' in query or 'exit' in query:
            speak("Goodbye!")
            break

        else:
            speak("Sorry, I didn't get that. Can you repeat?")

# Start Jarvis
if __name__ == "__main__":
    jarvis()
