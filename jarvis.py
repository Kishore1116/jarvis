import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Speech and Text-to-Speech Initialization
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon!")  
    else:
        speak("Good Evening!")
    speak("Jarvis here. How can I assist you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")  
        return "None"
    return query

# Email Sending Function
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email@gmail.com', 'your-password')
    server.sendmail('your-email@gmail.com', to, content)
    server.close()

# News Headlines Function
def getNews():
    news_url = "https://news.google.com/news/rss"
    news_feed = requests.get(news_url).text
    soup = BeautifulSoup(news_feed, 'html.parser')
    news_list = soup.find_all('item')
    for news in news_list[:5]:
        speak(news.title.text)
        print(news.title.text)
        speak("Moving on to the next news...")

# Telegram Bot Function
def start(update, context):
    update.message.reply_text("Hello! I'm Jarvis. How can I assist you?")

def handle_message(update, context):
    message = update.message.text
    response = process_message(message)
    update.message.reply_text(response)

def process_message(message):
    if 'wikipedia' in message:
        query = message.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia:\n{results}"
    elif 'news' in message:
        speak("Here are the top news headlines:")
        getNews()
        return "News headlines have been read aloud."
    elif 'email' in message:
        try:
            content = message.replace("email", "")
            to = "recipient-email@example.com"
            sendEmail(to, content)
            return "Email sent successfully."
        except Exception as e:
            print(e)
            return "Sorry, I couldn't send the email."
    else:
        return "I'm sorry, I didn't understand your request."

def main():
    updater = Updater('7381859403:AAGMC_0uvK_Uf34NTNJx6YNWvO203nCw6XY', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    wishMe()
    main()
