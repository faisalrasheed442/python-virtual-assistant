from __future__ import print_function
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import pickle
import datetime
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess
import wikipedia
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

MONTHS = ["january", "february", "march", "april", "may", "june","july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday","thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]

#Google Authentication


def Auth():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # replace token.pickle with ftoken you downloaded from google calendar
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # repalce the credentials.json with files you have downloaded from goolgle calendar
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


#to get event from google 
# 
# 
def get_event(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(), singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
#
    if not events:
        print('No upcoming events found.')
        speak("No upcoming events found")
    else:
        speak(f"you have {len(events)} envents on this day")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
            start_time = str(start.split("T")[1].split("-")[0])
            if int(start_time.split(":")[0]) < 12:
                start_time = start_time + "am"
            else:
                start_time = str(int(start_time.split(":")[0])-12)+ start_time.split(":")[1]
                start_time=start_time + "pm"
            speak(event["summary"]+"at"+start_time)

# speak function
#
#

def speak(text):
    run = pyttsx3.init()
    voices = run.getProperty('voices')
    x = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
    runvoices = run.setProperty('voice', x)
    run.say(text)
    run.runAndWait()

# get audio
#
#

def get_audio():
    loop=True
    while loop:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("I'm listing...\n")
            audio = r.listen(source)
            said = ""
            try:
                said = r.recognize_google(audio)
                print(said)
                loop=False
            except Exception as e:
                print("Exception:" + str(e))
                speak("i don't understand sir tell me again")
                loop=True
        print("Done Listing")
    return said


#get date from user
#
#


def get_date(num):
    num=num.lower()
    text=num
    today=datetime.date.today()
    if num.count("today")>0:
        return today
    month = -1
    day = -1
    week_day = -1
    year=today.year
    num = num.split()
    for x in num:
        if x in MONTHS:
            month=MONTHS.index(x)+1
        elif x.isdigit():
            day=int(x)
        elif x in DAYS:
            week_day=DAYS.index(x)
        else:
            for ext in DAY_EXTENTIONS:
                found=x.find(ext)
                if found>0:
                    try:
                        day=int(x[:found])
                    except:
                        pass
    if month < today.month and month !=-1:
        year=year+1
    if month ==-1 and day!=-1:
        if day<today.day:
            month=today.month+1
        else:
            month=today.month
    if month ==-1 and day ==-1 and week_day >=0:
        current_day=today.weekday()
        dif=week_day-current_day  
        if dif < 0:
            dif +=7
            if text.count("next")>=1:
                dif += 7
        return today + datetime.timedelta(dif)
    if day != -1:  
        return datetime.date(month=month, day=day, year=year)
#
# notpad
#
#
def note(text):
    date=datetime.datetime.now()
    myfile=str(date).replace(":","-")+"-note.txt"
    with open (myfile,"w") as k:
        k.writelines(text)
        k.close
#
#
#vlc player
def vlcc():
    vlc = "D:\music\music.m3u8"
    vl = "C:\Program Files\VideoLAN\VLC\\vlc.exe"
    subprocess.Popen([vl, vlc])
#
#
def browser(text):
    bro = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    d=f"google.com/?#q={text}"
    subprocess.Popen([bro,d])
# 

#wikipedia
def wiki(text):
    x=wikipedia.summary(text,sentences=2)
    print(x)
    speak(x)
#
#
#
#singing a song
def song():
    speak("Sir i can't sing")
    speak("can i help you with something else")
    y=get_audio()
    singing = "You're the light, you're the night You're the color of my blood You're the cure, you're the pain You're the only thing I wanna touch Never knew that it could mean so much, so much So love me like you do, lo-lo-love me like you do So love me like you do, lo-lo-love me like you do"
    so = ["insist", "i insist", "come on alex sing a song","sing a song"]
    for pharase in so:
        if pharase==y.lower():
            speak(singing)
            speak("i knew it sir i'm hilarious in singing but sir you made me do it, i won't sing again ")
            
#
#
#
def ext():
    loo=True
    while loo:
        speak("Sir do you want me to something else")
        text2=get_audio()
        reason=["yes","yup","ofcourse","why not","yes alex","yeah"]
        for phrase in reason:
            if phrase in text2.lower():
                loo=False
                return True
        if text2.lower()=="no":
            speak("good bye sir")
            loo=False
            exit()
        else:
            speak("i don't understand tell me again")
            loo=True

def main():
    loop=True
    while loop:
        speak("what can i do for you")
        loop=False
        text=get_audio()
        #calender function
        calnd = ["what do i have", "do i have","am i busy", "what will have on"]
        o=["i am busy"]
        for pharse in calnd:
            if pharse in text.lower():
                y=get_date(text)
                service=Auth()
                get_event(y,service)
                loop=ext()
                break
        #owner function here
        #
        owner = ["who made you", "who created you", "who is you owner"]
        for pharse in owner:
            if pharse in text.lower():
                speak("i am created by faisal malik")
                loop = ext()
                break
        #name function here
        #
        #
        name = ["what is your name", "what do i call you", "which name was given you",
                "do you have any name", "what can i call you", "what we call you"]
        for pharse in name:
            if pharse in text.lower():
                speak("My name is Axel")
                loop = ext()
                break
        notee=["take a note","get a note","write a note"]
        for pharse in notee:
            if pharse in text.lower():
                speak("tell me what do you want me to take note about")
                u=get_audio()
                note(u)
                loop=ext()
                break
        music=["play some music","music","axel play music","axel music"]
        for pharse in music:
            if pharse in text.lower():
                vlcc()
                exit()
                break
        brows=["search on google","axel google","do some searching on google"]
        for pharse in brows:
            if pharse in text.lower():
                speak("sir what do you want search")
                s=get_audio()
                browser(s)
                loop=ext()
        wikii=["alex search on wiki","alex search on wikipedia","wiki","wikipedia","search on wikipedai",]
        for pharase in wikii:
            if pharase==text.lower():
                speak("sir what do you want to search on wikipeida")
                r=get_audio()
                wiki(str(r))
                loop=ext()
        si=["sing a song","alex sing a song",]
        for pharase in si:
            if pharase==text.lower():
                song()
                loop=ext()        
        chek = 2
        if chek == 1:
            pass
        else:
            
            loop = True
main()         
