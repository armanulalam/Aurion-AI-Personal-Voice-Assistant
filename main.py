# import dependencies
import pyttsx3
import speech_recognition as sr
import datetime
import os
import logging
import webbrowser
import wikipedia
import random
import subprocess
import google.generativeai as genai
import winsound
import requests
import difflib
import smtplib
import pywhatkit.whats as whatsapp
from contact_email import is_in_email_contact, get_email_add
from contact_whatsapp import IsInContact,get_mobile_or_group,IsGroup

# logging configuration
LOG_DIR = 'logs'
LOG_FILE_NAME = 'application.log'

os.makedirs(LOG_DIR, exist_ok = True) # make the directory
log_path = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename = log_path,
    format = "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

# activating voice from local machine
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 160)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# speak function
def speak(text):
    """
    This function converts the text to voice

    Args: 
        text
    returns:
        voice
    """
    engine.say(text)
    engine.runAndWait()

# this function recognize the user's speech and coverts the speech to text
def takeCommand():
    """
    This function take command from the users and recognize the voice

    returns:
        text as user query
    """

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening......")
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("Recognizing......")
        query = r.recognize_google(audio, language = "en-in")
        print(f"User said: {query}")

    except Exception as e:
        logging.info(e)
        print("Kindly repeat what you said before. I could not quite catch you.")
        return "None"

    return query


# this function greets the user based on time
def greeting():
    hour = (datetime.datetime.now().hour)

    if hour >= 0 and hour < 12:
        speak("Good Morning sir!! How are you doing??")
        read_schedule() #auto reading schedule every morning
    elif hour >= 12 and hour <= 18:
        speak("Good Afternoon sir!! How are you doing??")
    else:
        speak("Good Evening sir!! How are you doing??")


    speak("Sir, I am Aurion.. I am your personal AI voice assistant.. How may I help you today?")

# this function plays a random music from the music folder
def play_music():
    music_directory = "E:\AI Voice Assistant\music"

    try:
        songs = os.listdir(music_directory)

        if songs:
            random_song = random.choice(songs)
            speak(f"Playing the song randomly from your music folder and the song name is {random_song}")
            os.startfile(os.path.join(music_directory,random_song))
            logging.info(f"Playing music: {random_song}")

        else:
            speak("No music files are found in your music directory")

    except Exception:
        speak("Sorry sir!! I could not able to find your music folder.")

def gemini_response(user_input):
    GOOGLE_API_KEY = "" # your google studio ai api key
    genai.configure(api_key = GOOGLE_API_KEY)

    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"You are an intelligent personal assistant named Aurion..Your creator will ask you questions,you will have to answer in only 2 to 3 sentences very concisely and to the point. Question:{user_input}"
    response = model.generate_content(prompt)

    return response.text
 
def add_schedule():
    speak("What should I add to your to your schedule for today?")
    task = takeCommand()

    if task == "None":
        speak("I didn't catch that, please try again.")
        return
    

    with open("schedule.txt",'a') as f:
        f.write(task + '\n')

    speak("Task added to today's schedule.")

def read_schedule():
    if not os.path.exists('schedule.txt'):
        speak("You have no tasks schedule for today.")
        return 
    
    with open('schedule.txt','r') as f:
        tasks = f.readlines()

    if len(tasks) == 0:
        speak("Your schedule is empty for today.")
        return
    
    speak("Here is your schedule for today.")

    for i,tasks in enumerate(tasks,1):
        speak(f"Task {i} is {tasks.strip()}")

def clear_schedule():
    open('schedule.txt','w').close()
    speak("Today's schedule has been deleted.")

def set_reminder():
    speak("What should I remind you about?")
    reminder_text = takeCommand()

    speak("When should I remind you? Plaese say the time in HH:MM format")
    reminder_time = takeCommand()

    try:
        datetime.datetime.strptime(reminder_time, "%H:%M")

        with open('reminders.txt','a') as f:
            f.write(f"{reminder_time} - {reminder_text}\n")

        speak(f"Reminder set for {reminder_time}")

    except ValueError:
        speak("Invalid time format..Please say something like 18 30 or 06 25")

def check_reminders():
    now = datetime.datetime.now().strftime("%H:%M")

    if not os.path.exists("reminders.txt"):
        return
    
    with open("reminders.txt", 'r') as f:
        lines = f.readlines()

    new_list = []
    for line in lines:
        times, text = line.split(" - ")

        if times == now:
            speak(f"Sir, a reminder to you for {text}")

        else:
            new_list.append(line)

    with open("reminders.txt", "w") as f:
        f.writelines(new_list)

def set_alarm():
    speak("Please say the time for alarm in HH:MM format")
    alarm_time = takeCommand().replace(" ", "").strip() 

    if len(alarm_time) == 4 and alarm_time.isdigit():
        alarm_time = alarm_time[:2] + ":" + alarm_time[2:]

    try:
        datetime.datetime.strptime(alarm_time, "%H:%M")

        with open('alarms.txt','a') as f:
            f.write(alarm_time+"\n")

        speak(f"Alarm set for {alarm_time}\n")

    except ValueError:
        speak("Invalid time format..Please try again!")


def check_alarms():
    now = datetime.datetime.now().strftime("%H:%M")

    if not os.path.exists("alarms.txt"):
        return
    
    with open("alarms.txt", 'r') as f:
        alarms = f.readlines()

    remains = []
    for alarm in alarms:
        alarm = alarm.strip()

        if alarm == now:
            speak(f"Wake up sir! Your alarm is ringing..")
            beep_alarm()

        else:
            remains.append(alarm+"\n")

    with open("alarms.txt", "w") as f:
        f.writelines(remains)


def beep_alarm():
    for _ in range(6):
        winsound.Beep(2000,1000)

TODO_File = "todo.txt"

if not os.path.exists(TODO_File):
    with open(TODO_File,'w') as f:
        pass

def add_task(task):
    with open(TODO_File,'a') as f:
        f.write(task+'\n')
    speak(f"{task} has been added")

def show_task():
    if os.path.getsize(TODO_File) == 0:
        speak("Your to do list is empty.")
        return
    
    speak("Your to do list show in the screen")
    with open(TODO_File,'r') as f:
        tasks = f.readlines()

    for i,task in enumerate(tasks,1):
        print(f"{i}. {task.strip()}")


def remove_task():
    speak("Which task should I remove?")
    spoken = takeCommand().lower().strip()

    with open(TODO_File, 'r') as f:
        tasks = [t.strip() for t in f.readlines()]

    if not tasks:
        speak("Your task list is empty.")
        return

    match = difflib.get_close_matches(spoken, tasks, n=1, cutoff=0.4)

    if match:
        task_to_remove = match[0]
        tasks.remove(task_to_remove)

        with open(TODO_File, 'w') as f:
            for t in tasks:
                f.write(t + "\n")

        speak(f"Task '{task_to_remove}' has been removed.")
    else:
        speak("I could not find that task.")


def clear_tasks():
    open(TODO_File,'w').close()
    speak("All tasks deleted.")

NEWS_API_KEY = "" # your news api key
GOOGLE_API_KEY = "" # your google studio ai api key
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_news(topic):
    url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"

    try:
        response = requests.get(url).json()

        if response['status'] != 'ok' or not response['articles']:
            speak(f"Sorry! I couldn't find news about {topic}")
            return
        speak(f"Here are the latest news about {topic}")
        i = 0
        for article in response['articles'][:3]:
            title  = article['title']
            description = article.get('description',"")
            content = article.get('content',"")
            i += 1

            speak(f"Headline: {title}")
            summary_prompt = f"Summarize this news in 3 to 4 lines:\n\nTitle: {title}\n\nDescription: {description}\n\nContent: {content}"
            summary = model.generate_content(summary_prompt).text
            speak(f"Summary: {summary}")
            if i < 3:
                speak("Next headline.")

    except Exception as e:
        speak("Sorry, I failed to fetch the news.")
        print(e)

EmailAppPass = "" # your email app password

def send_email(to,msg):
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.connect("smtp.gmail.com",587)
    mail.ehlo()
    mail.starttls()
    mail.ehlo()
    mail.login("alamarmanul64@gmail.com",EmailAppPass)
    mail.sendmail("alamarmanul64@gmail.com",to,msg)
    mail.close()

def send_msg_whatsapp_group(id,msg):
    whatsapp.sendwhatmsg_to_group_instantly(id,msg,wait_time=5)

def send_msg_whatsapp_individual(mobile,msg):
    whatsapp.sendwhatmsg_instantly(mobile,msg,wait_time=5)


greeting()

while True:
    query = takeCommand().lower()
    print(query)

    if "your name" in query:
        speak("My name is Aurion..")

    elif "time" in query:
        time = datetime.datetime.now().strftime("%H:%M.%S")
        speak(f"Sir, the time is {time}")
        logging.info("User asked for current time")

    elif "how are you" in query:
        speak("I am fine sir.. I am always here to help you..")
        logging.info("User asked about Aurion's well-being")

    elif "who made you" in query:
        speak("I am created by Armanul Alam sir..")
        logging.info("User asked about the creator of the assistnt.")
    
    elif "thank you" in query:
        speak("My pleasure!! I am always happy to help you..")
        logging.info("User expressed gratitude.")
    
    elif "wikipedia" in query:
        speak("I am searching from wikipedia.. Wait for a moment sir..")
        query = query.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences = 3)
        speak("According to wikipedia,")
        speak(result)
        logging.info("User requested information from wikipedia.")

    elif "open google" in query:
        speak("I am opening google..Wait for a moment..")
        webbrowser.open("google.com")
        logging.info("User asked for opening google.")

    elif "open calculator" in query or "calculator" in query:
        speak("I am opening calculator!!")
        subprocess.Popen("calc.exe")
        logging.info("User requested to open calculator.")
    
    elif "open notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")
        logging.info("User requested to open Notepad.")
    
    elif "open terminal" in query or "open cmd" in query:
        speak("Opening Command Prompt terminal")
        subprocess.Popen("cmd.exe")
        logging.info("User requested to open Command Prompt.")
    
    elif "open calendar" in query or "calendar" in query:
        speak("Opening Google Calendar")
        webbrowser.open("https://calendar.google.com")
        logging.info("User requested to open Calendar.")

    elif "youtube" in query:
        speak("Opening youtube for you sir..")
        query_list = []
        for i in query.split():
            if i not in ['search','on','in','youtube']:
                query_list.append(i)

        query = " ".join(query_list)
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        logging.info("User requested to open youtube.")

    elif "jokes" in query:
        with open("jokes.txt",'r') as f:
            jokes_list = []
            for joke in f:
                jokes_list.append(joke)

        joke = random.choice(jokes_list)
        speak(joke)
        logging.info("User requested to tell a joke.")

    elif "play music" in query or "play a music" in query:
        speak("Okay sir.. I am randomly playing a song.")
        play_music()

    elif "exit" in query or "good bye" in query or "goodbye" in query:
        speak("Thanks for your time sir.. Have a great day!")
        logging.info("User exited from the program.")
        exit()

    elif "add schedule" in query or "add to my schedule" in query:
        add_schedule()
        logging.info("User asked for adding in schedule.")
    
    elif "read schedule" in query or "today's schedule" in query:
        read_schedule()
        logging.info("User asked for reading schedule.")

    elif "clear schedule" in query or "delete schedule" in query:
        clear_schedule()
        logging.info("User asked for delete the schedule.")

    elif "set reminder" in query or "remind me" in query:
        set_reminder()
        logging.info("User asked for reminding.")
    
    elif "set alarm" in query:
        set_alarm()
        logging.info("User asked for to set alarm.")

    elif "add task" in query:
        speak("Tell me the task.")
        task = takeCommand()
        add_task(task)
        logging.info("User asked for add task.")

    elif "show to do list" in query or "show tasks" in query:
        show_task()
        logging.info("User asked for show tasks")

    elif "remove task" in query or "delete tasks" in query:
        remove_task()
        logging.info("User asked for remove tasks.")

    elif "clear all tasks" in query or "delete all tasks" in query:
        clear_tasks()
        logging.info("User asked for clear tasks.")

    elif "read news" in query:
        speak("What topic should I find news about?")
        topic = takeCommand().lower()
        get_news(topic)
        logging.info("User asked for reading news.")

    elif 'send' in query and 'email' in query:
        speak("Whom you want to send an email?")
        statement = takeCommand().lower()

        if is_in_email_contact(statement):
            speak("What is the message you want to send?")
            msg = takeCommand()
            to = get_email_add(statement)
            send_email(to,msg)

        else:
            speak(get_email_add(statement))
        logging.info("User asked to send an email.")

    elif ("send" in query and 'whatsapp' in query) or ("message" in query and "whatsapp" in query):
        speak("Whom you want to send message via Whatsapp?")
        person = takeCommand()

        if IsInContact(person):
            contact_info = get_mobile_or_group(person)
            speak("What message you want to send?")
            msg = takeCommand()
            if IsGroup(person):
                send_msg_whatsapp_group(contact_info, msg)
            else:
                send_msg_whatsapp_individual(contact_info, msg)

        else:
            speak(get_mobile_or_group(person))

        logging.info("User asked to send whatsapp message.")


    else:
        response = gemini_response(query)
        speak(response)
        logging.info("User asked question to the Gemini.")

    check_reminders()
    check_alarms()

