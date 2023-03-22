from pickletools import uint1
from plistlib import UID
import pyttsx3
import tkinter
import datetime
import PyPDF2
import speech_recognition as sr
import wikipedia
import operator
import pywhatkit as kit
import smtplib
import json
import pyautogui
import webbrowser
import pyjokes
from bs4 import BeautifulSoup
import winshell
import subprocess
import os
import random
import re
import requests
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from gui import Ui_MainWindow
import threading
import sys






# ------------ Taking Voice Input ------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# ------------ Use voices[0] for male voice  &  voices[1] for female voice ------------
engine.setProperty('voice', voices[0].id)


# ------------ Function for Assistant Speaking ----------
def speak(audio):
    ui.updateMoviesDynamically("Speaking")
    engine.say(audio)
    ui.terminalPrint(audio)
    engine.runAndWait()


#----------- Function to read -----------
def pdf_reader():
    book= open('C:\\Users\\Gaurav Thakur\\Downloads\\final.pdf','rb')
    pdfReader=PyPDF2.PdfFileReader(book);
    pages = pdfReader.numPages
    speak(f"Total numbers of pages in this book{pages}")
    pg=int(input("Please enter the page number: "))
    page=pdfReader.getPage(pg)
    text=page.extractText()
    speak(text)
    
    
#----------- Function to send mail -----------
def sendemail(to,content):
    server=smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("thakurgauravgt.7355@gmail.com", "hpvtdakdahdhqtui")
    server.sendmail("thakurgauravgt.7355@gmail.com", to, content)
    server.close()


#----------- Function to find my location -----------
def My_Location():
    print("Checking........")
    ip_add = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'   
    geo_q = requests.get(url)    
    geo_d = geo_q.json()    
    state = geo_d['city']    
    country =geo_d['country']
    speak(f"Sir, you are now in {state,country}.")
    

#----------- Function to take ScreenShot -----------
def screenshot():
    img = pyautogui.screenshot()
    img.save("E:\\Gaurav\\Projects\\Jarvis\\jarvis_ss\\js.png")



# ------------ Function to Greet your Master ------------
def wishMe():
    ui.updateMoviesDynamically("Speaking")
    hour = int(datetime.datetime.now().hour)
    if hour >= 3 and hour < 12:
        speak('Good Morning')
    elif hour >= 12 and hour < 16:
        speak('Good Afternoon')

    else:
        speak('Good Evening')
        speak('Pratibha maam and Ranjan Sir. I am your personal assistant, Please tell me how may I help you')


class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()
        
        
        # ------------ Function to Listen & Recognize ----------
    def takeCommand(self):
        ui.updateMoviesDynamically("Listening")
        # it take microphone input from user and return string output
        r = sr.Recognizer()
        with sr.Microphone() as source:
            ui.terminalPrint('Listening.....')
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            ui.updateMoviesDynamically("loading") 
            ui.terminalPrint('Recognizing')
            query = r.recognize_google(audio, language='en-in')
            ui.terminalPrint(f'User said: {query}\n')

        except Exception as e:
            # print(e)
            ui.terminalPrint('Say that again plese.....')
            return 'None'
        return query
         
         
# ----------- Function to read -----------
    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()

        # ------ logic for executing task based on query ------

        # --- search on wikipedia ---
            if 'wikipedia' in self.query:
                speak('Searching wikipedia')
                self.query = self.query.replace('wikipedia', '')
                results = wikipedia.summary(self.query, sentences=2)
                speak('According to wikipedia')
                ui.terminalPrint(results)
                speak(results)

        # --- Open Youtube ---
            if 'open youtube' in self.query:
                webbrowser.open('www.youtube.com')

        # --- Open Google ---
            elif 'open google' in self.query:
                webbrowser.open('google.com')

        # --- Open StackOverflow ---
            elif 'open stack overflow' in self.query:
                webbrowser.open('stackoverflow.com')

        # --- Search query on Default webBrowser ---
            elif 'search' in self.query:
                speak('Searching' + self.query)
                webbrowser.open_new_tab(self.query)

        # --- Weather in particular City ---
            elif 'weather' in self.query or 'tempature' in self.query:
                url = f"https://www.google.com/search?q={self.query}"
                k = requests.get(url)
                data = BeautifulSoup(k.text, "html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"The {self.query} is {temp}")

        # --- Read PDF ---
            elif "read pdf" in self.query:
                pdf_reader()  
            
        # --- Take ScreenShot ---
            elif 'screenshot' in self.query:
                speak("taking screenshot")
                screenshot()
            
        # --- Find My Location ---
            elif 'my location' in self.query:
                My_Location()
            

        # --- Play Music fron local File
            elif 'play music' in self.query:
                music_dir = 'D:\\Music PlayList'
                songs = os.listdir(music_dir)
                ui.terminalPrint(songs)
                random = os.startfile(os.path.join(music_dir, songs[1]))
                
                
        # --- Perform Mathematical Calculation ---
            elif "do some calculation" in self.query or "can you calculate" in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, example: 2 plus 2")
                    print("listening......")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return{
                        '+' : operator.add, #plus
                        '-' : operator.sub, #minus
                        '*' : operator.mul, #multiplied by
                        '/' : operator.__truediv__, #divided
                    }[op]
                def eval_binary_expr(op1, oper, op2): # 2 plus 2
                    op1,op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1,op2)
                speak("your result is")
                speak(eval_binary_expr(*(my_string.split())))
            
            # --- send email ---
            elif "send email" in self.query or "email" in self.query or "mail" in self.query:           
                try:
                    speak("what should i say")
                    content = self.takeCommand()
                    
                    to = (input("Enter the destination email id: "))
                    
                    sendemail(to,content)
                    speak("Email has been sent sccessfully.")
                    
                except Exception as e:
                    print(e)
                    speak("Email has not been sent due to some exception.")
                
            # --- send whatsApp Message ---
            elif "send message" in self.query:
                try:
                    speak(f"Please Enter the Phone Number")
                    num=(input("Enter the Phone Number: "))
                    r = sr.Recognizer()
                    with sr.Microphone() as source:
                        speak("Say what you want to message, example: Hello! how are you ?")
                        print("listening......")
                        r.adjust_for_ambient_noise(source)
                        audio = r.listen(source)
                    my_string = r.recognize_google(audio)
                    print(my_string)
                    speak(f"Please Enter the Time of message,")
                    hr=int(input("Enter the Hour Clock, example: 10 "))
                    min=int(input("Enter the min Clock, example: 48 "))
                    kit.sendwhatmsg(num,my_string,hr,min)
                
                except Exception as e:
                    print(e)
                    speak("Email has not been sent due to some exception.")
                    
        # --- Current Time ---
            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"sir, the time is {strTime}")

        # --- Exit from progrm ---
            elif 'exit' in self.query:
                speak("Thanks for giving me your time , have a nice day")
                exit()

        # --- Owner's Name ---
            elif "who made you" in self.query or "who created you" in self.query or "who is your master" in self.query:
                speak("I have been created by Group 8, under the guidence of Pratibha ma'am ")

        # --- For entertainment purpose ---
            elif "joke" in self.query:
                speak(pyjokes.get_joke())

        # --- Empty Recycle Bin ---
            elif 'empty recycle bin' in self.query:
                winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
                speak("Recycle Bin Recycled")

        # --- Restart PC ---
            elif "restart" in self.query:
                subprocess.call(["shutdown", "/r"])


# ------------ End Of Program ------------


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.RunButton.clicked.connect(self.startTask)
        self.ui.EnterButton.clicked.connect(self.manualCodeFromTerminal)
        self.ui.ExitButton.clicked.connect(self.close)
        self.ui.GoogleButton.clicked.connect(self.google)
        self.ui.YoutudeButton.clicked.connect(self.youtube)
        self.ui.WhatsappButton.clicked.connect(self.whatsapp)
        
    
    

    def startTask(self):
        self.ui.movie = QtGui.QMovie("T8bahf.gif")
        self.ui.IntGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("ApiG.gif")
        self.ui.RoboGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("listining.gif")
        self.ui.SpeakingGif_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("UGEY.gif")
        self.ui.FloatingGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("Speaking.gif")
        self.ui.SpeakingGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("Loading.gif")
        self.ui.SleepGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("sleep mode.gif")
        self.ui.SleepingGif.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        self.ui.movie = QtGui.QMovie("bot.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        TimeLabel = current_time.toString('hh:mm:ss')
        DateLabel = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(TimeLabel)
        self.ui.textBrowser_2.setText(DateLabel)
        
    
            
        
        
    def updateMoviesDynamically(self, state):
        if state == 'Listening':
            self.ui.SpeakingGif.raise_()
            self.ui.SpeakingGif_2.hide()
            self.ui.SleepGif.hide()
            self.ui.SleepingGif.hide()
            self.ui.SpeakingGif.show()
            
        elif state == 'Speaking':
            self.ui.SpeakingGif_2.raise_()
            self.ui.SpeakingGif.hide()
            self.ui.SleepGif.hide()
            self.ui.SleepingGif.hide()
            self.ui.SpeakingGif_2.show()
            
            
        elif state == 'loading':
            self.ui.SleepGif.raise_()
            self.ui.SpeakingGif.hide()
            self.ui.SleepingGif.hide()
            self.ui.SleepingGif.hide()
            self.ui.SleepGif.show()
            
        elif state == 'Sleeping':
            self.ui.SleepingGif.raise_()
            self.ui.SpeakingGif.hide()
            self.ui.SleepGif.hide()
            self.ui.SpeakingGif_2.hide()
            self.ui.SleepingGif.show()

        
        
    def google(self):
        webbrowser.open('google.com')
        
    def youtube(self):
        webbrowser.open('www.youtube.com')
        
    def whatsapp(self):
        webbrowser.open('web.whatsapp.com')
        
    def terminalPrint(self, text):
        self.ui.OutputTerminal.appendPlainText(text)    
        
    def manualCodeFromTerminal(self):
        query = self.ui.InputTerminal.text()
        if query:
            self.ui.InputTerminal.clear()
            self.ui.OutputTerminal.appendPlainText(f"You Just typed>>{query}")
               
            if query =='exit':
                ui.close()
            
            elif query == 'help':
                self.terminalPrint("i can help you")
                    
            else:
                pass
            
app = QApplication(sys.argv)
ui = Main()
ui.show()
exit(app.exec_())