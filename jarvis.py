import pyttsx3
import speech_recognition as sr
import datetime
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)

    try:
        print("Wait for few Moments...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You just said: {query}\n")
    except Exception as e:
        print(e)
        speak("Please Tell me again")
        query = "none"
    return query

def wishings():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        return "Good Morning BOSS"
    elif hour >= 12 and hour < 17:
        return "Good Afternoon BOSS"
    elif hour >= 17 and hour < 21:
        return "Good Evening BOSS"
    else:
        return "Good Night BOSS"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(wishings())

def handle_message(update: Update, context: CallbackContext):
    query = update.message.text.lower()
    if 'time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"Sir, the time is {strTime}"
    elif 'open firefox' in query:
        response = "Opening firefox Application sir..."
        # Adjust or remove this line based on Android capabilities
        # os.startfile() is not supported in Termux
    elif 'wikipedia' in query:
        try:
            import wikipedia
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=1)
            response = f"According to Wikipedia, {results}"
        except:
            response = "No results found."
    else:
        response = "I don't understand that command."

    update.message.reply_text(response)
    speak(response)

def main():
    TOKEN = '7381859403:AAGMC_0uvK_Uf34NTNJx6YNWvO203nCw6XY'
    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
