import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from PyDictionary import PyDictionary
import random
import plyer as pl
from youtubesearchpython import VideosSearch



PRESENTATION: str =  '''Hello! I am Adam. I am a desktop assistance created by Abdallah Zerfaoui. 
I can perform various tasks like opening an app, setting reminder, open websites in browser, 
search in wikipedia, search a video in youtube, search a query in google and so on.
Before telling me task you have to say, 'hey Adam' to enter task-mode, and after completion you have to say,
'thank you Adam', to exit task mode. In the same task mode you can ask me to play music or even to play 
a video on youtube and I will do it immediately. I can even send emails to specified clients. 
I can tell you the current time whenever you ask me in task-mode. 
I have some in built features like water reminder that will remind you to take a short break every 30 mins 
and word for the day feature that will show you a random english word with its meaning. 
To exit from the program say "goodbye Adam". 
Thank you! Special thanks to the developers of the modules and packages that were used in my creation.'''


class DesktopAssistant():
    def __init__(self):
        self.language = 'en_in'
        self.engine = pyttsx3.init('sapi5')
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[0].id) # Choose voice number 0
                                                  #3 is french accent

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    

    def wishMe(self, start):
        hour = int(datetime.datetime.now().hour)
        if start == True:
            if hour >= 0 and hour < 12:
                self.speak = self.speak("Good Morning!")

            elif hour >= 12 and hour < 18:
                self.speak("Good Afternoon!")
    
            else:
                self.speak("Good Evening!")

            self.speak("I am Adam Sir. Good to see you again.")
        else:
            self.speak('Goodbye sir')
            if hour >= 0 and hour < 12:
                self.speak("Have a good day!")

            elif hour >= 18 and hour < 24:
                self.speak("Have a good night!")


    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source) #the command

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language = self.language)
            print(f"User said: {query}\n")

        except Exception as e:
            print("Say that again please...")
            return "None"
        return query


    def sendEmail(self, to, content):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('omkar.kulkarni20@vit.edu', '12010457@ok')
        server.sendmail('omkar.kulkarni20@vit.edu', to, content)
        server.close()


    def waterReminder(self):
        M = int(datetime.datetime.now().minute)
        if M == 0 or M == 30:
            pl.notification.notify(
                title='Break Reminder.',
                message='Hey, take a break and drink some water.',
                timeout=60
            )
            self.speak("Hello sir, time to take a short break")


    def setReminder(self, reminders):
        self.speak("At what time do you want me to remind you?")
        reminder_time = self.takeCommand().lower()
        self.speak('What do you want me to remind you of?')
        content = self.takeCommand()

        try:
            reminder_time = reminder_time.replace(':', ' ').split()
            reminder_time[0], reminder_time[1] = int(reminder_time[0]), int(reminder_time[1])
            if ('p.m.' in reminder_time) and reminder_time[0] < 12:
                reminder_time[0] += 12
            elif 'a.m.' in reminder_time and reminder_time[0] == 12:
                reminder_time[0] = 0
            reminder_time[2] = content
            reminders.append(reminder_time)
            self.speak('Reminder was successfully set')
        except:
            self.speak('Could not set the reminder')


    def checkReminder(self, reminders):
        H = int(datetime.datetime.now().hour)
        M = int(datetime.datetime.now().minute)
        for timestamp in reminders:
            if H == timestamp[0] and M == timestamp[1]:
                pl.notification.notify(
                    title='Reminder from Adam',
                    message=timestamp[2],
                    timeout=60,
                    app_icon='Adam.ico'
                )
                self.speak(f'Sir, here  is a reminder to {timestamp[2]}')
                reminders.remove(timestamp)


    def wordForTheDay(self):
        while True:
            f = open('words.txt', 'r')
            wordlist = f.readlines()
            f.close()
            word = wordlist[random.randint(0, 10000)]
            meanings = PyDictionary.meaning(word)
            try:
                means = '\n'.join(value[0] for value in meanings.values())
                break
            except:
                pass
        pl.notification.notify(
            title='Word for the Day',
            message=f'{word.capitalize()} {means}',
            timeout=60,
            app_icon='Adam.ico'
        )

    ### TASK FUNCTIONS #######
    def search_in_browser(self, query):
        try:
            search_query = query.replace('search in browser', '')
            webbrowser.open(f'https://www.google.com/search?q={search_query}')
            self.speak('Searching the web for ' + search_query)
        except Exception as e:
            print(e)
            self.speak('Could not perform the web search. Please try again.')


    def search_in_youtube(self, query):
        try:
            search_query = query.replace('search in youtube', '')
            webbrowser.open(f'https://www.youtube.com/results?search_query={search_query}')
            self.speak('Searching YouTube for ' + search_query)
        except Exception as e:
            print(e)
            self.speak('Could not perform the YouTube search. Please try again.')


    def search_in_wikipedia(self, query):
        try:
            search_query = query.replace("search in wikipedia", "")
            summary = wikipedia.summary(search_query, sentences=2)
            self.speak("According to Wikipedia")
            print(summary)
            self.speak(summary)
        except Exception as e:
            print(e)
            self.speak('Could not retrieve information from Wikipedia. Please try again.')

    ### END TASK FUNCTIONS ###
    def Tasks(self, query):
        if 'search in browser' in query:
            self.search_in_browser(query)

        elif 'search in youtube' in query:
            self.search_in_youtube(query)

        elif 'search in wikipedia' in query:
            self.search_in_wikipedia(query)

        elif 'open youtube' in query:
            try:
                webbrowser.open("youtube.com")
            except:
                self.speak('Could not perform the task. Please try again.')

        elif 'play in youtube' in query:
            try:
                query = query.replace('play in youtube', '')
                videosSearch = VideosSearch(query, limit=1)
                url = videosSearch.result()['result'][0]['link']
                webbrowser.open(url)
            except:
                self.speak('Could not perform the task. Please try again.')

        elif 'open google' in query:
            try:
                webbrowser.open("google.com")
            except:
                self.speak('Could not perform the task. Please try again.')

        elif 'open stackoverflow' in query:
            try:
                webbrowser.open("stackoverflow.com")
            except:
                self.speak('Could not perform the task. Please try again.')

        elif 'open v i e r p' in query:
            try:
                webbrowser.open("learner.vierp.in/home")
            except:
                self.speak('Could not perform the task. Please try again.')

        elif 'play music' in query:
            music_dir = 'D:\\Music\\timepass'
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'what is the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            self.speak(f"Sir, the time is {strTime}")

        elif 'open vs' in query:
            codePath = "C:\\Users\\omkar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'open whatsapp' in query:
            codePath = "C:\\Users\\omkar\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
            os.startfile(codePath)

        elif 'email to xyz' in query:
            try:
                self.speak("What should I say?")
                content = self.takeCommand()
                to = "xyz@gmail.com"
                self.sendEmail(to, content)
                self.speak("Email has been sent!")
            except Exception as e:
                print(e)
                self.speak("Sorry, could not send the email.")


if __name__ == "__main__":
    my_desk_assistant = DesktopAssistant()
    my_desk_assistant.wishMe(True)
    #my_desk_assistant.wordForTheDay()
    reminders = []
    while True:
        # if 1:
        #my_desk_assistant.process_audio_input()
        query = my_desk_assistant.takeCommand().lower()
        print("that's what i hear", query)

        if "switch to french" in query:
            my_desk_assistant.language = "fr-FR"
            print(my_desk_assistant.language)

        if "passer" in query and "anglais" in query:
            my_desk_assistant.language = "en-in"
            print(my_desk_assistant.language)

        # Logic for executing tasks based on query
        if "hey adam" in query:
            my_desk_assistant.speak('hello sir! How can I help you?')

            while True:
                query = my_desk_assistant.takeCommand().lower()

                if 'set reminder' in query or 'set a reminder' in query:
                    my_desk_assistant.setReminder(reminders)

                my_desk_assistant.Tasks(query) # main part

                if 'introduce yourself' in query:
                    my_desk_assistant.speak(PRESENTATION)

                elif 'thank you adam' in query:
                    my_desk_assistant.speak('You are welcome sir!')
                    break

                my_desk_assistant.waterReminder()
                my_desk_assistant.checkReminder(reminders)

        my_desk_assistant.waterReminder()
        my_desk_assistant.checkReminder(reminders)

        if 'goodbye' in query and 'adam' in query:
            my_desk_assistant.wishMe(False)
            exit(0)