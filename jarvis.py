import pyttsx3
import speech_recognition as sr
import webbrowser
import pyautogui
import random
import requests
import google.generativeai as genai
import datetime
from keys import WEATHER_API_KEY, GEMINI_API_KEY, NEWS_API_KEY

#to speak what you have listen  
engine=pyttsx3.init()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def listen():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening")
        audio=r.listen(source)
        try:
            print("Recognizing")
            text=r.recognize_google(audio)
            return text
        except: 
            print("unable to recognize")
            speak("unable to recognize")
            return "unable to recognize"


def speak(query):
    engine.say(query)
    engine.runAndWait()


def search(query):
    print(query)
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

def greet():
    hour = datetime.datetime.now().hour
    if hour>= 0 and hour<12:
        print("Jarvis : Good Morning ")
        speak("Good Morning")
    elif hour>= 12 and hour<16:
        print("Jarvis : Good Afternoon ")
        speak("Good Afternoon")
    else:
        print("Jarvis : Good Evening ")
        speak("Good Evening")

    print("\t My name is Jarvis, How can I help you")
    speak("My name is Jarvis, How can I help you")
    

if __name__ == "__main__":

    greet()
    while True:

        query = listen().lower()

        if("unable") in query:
            exit()


        print(f"Afnan : {query}")
        sites = ["youtube", "facebook", "instagram", "chatgpt", "wikipedia"]
        
        if "open" in query:
            for site in sites:
                if site in query:
                    webbrowser.open(f"{site}.com")
        
        elif "google" in query:
            text = query.split()
            text.remove("google")
            search(" ".join(text))
        
        elif "screenshot" in query:
            r = random.randint(0, 501)
            screenshot = pyautogui.screenshot()
            screenshot.save(f'C:\\Users\\user\\OneDrive\\Desktop\\ultimate 01\\dictionary\\screenshot{r}.png')

        elif ("weather" or "temperature") in query:
            city = query.split()
            city = city.pop()
            url = f"https://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"Jarvis : The temperature of {city} is {data['current']['temp_c']} degree Celsius and the Weather is {data['current']['condition']['text']}.")
                speak(f"The temperature of {city} is {data['current']['temp_c']} degree Celsius and the Weather is {data['current']['condition']['text']}.")
            else:
                print(f"Jarvis : Sorry, the Location is Invalid")
                speak("Sorry, the Location is Invalid")

        elif ("news" or "headlines") in query:

            date = datetime.datetime.now().date()
            url = f"https://newsapi.org/v2/top-headlines?country=in&from={date}&sortBy=popularity&apiKey={NEWS_API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                
                for i in range(4):
                    article = data['articles'][i]
                    title = article['title']
                    source = article['source']['name']
                    print(f"Title: {title}")
                    speak(f"Title: {title}")
                    print(f"Source: {source}")
                    speak(f"Source: {source}")
                    print()


        elif ("write" or "program") in query:
            response = model.generate_content(query)
            content = response.text
            content = content.replace('*','').replace('#','')
            with open(f'{query[5:]}__.txt','w') as file:
                file.writelines(response.text)

            print(f"Jarvis : The Program has been written in file")
            speak("The Program has been written in file")


        elif ("quit" or "exit" or "terminate") in query:
            print("Jarvis : Thank you sir for Interacting with me")
            speak("Thank you for Interacting with me")
            exit()

        else: 
            response = model.generate_content(query)
            content = response.text[:700]
            content = content.replace('*','').replace('#','')
            print(f"Jarvis : {content}")
            speak(f"{content}")