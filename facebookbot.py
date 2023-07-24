
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import PySimpleGUI as sg
import os
import time
from time import sleep

PATH = "F:\chromedriver.exe"
option1 = Options()
option1.add_argument("--disable-notifications")


class FacebookBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(PATH,chrome_options=option1)
        self.driver.maximize_window()
        self.login()

    def login(self):
        
        self.driver.get('https://www.facebook.com/')#Naviagtes to the facebook info page
        time.sleep(2)
        self.driver.find_element(By.NAME,"email").send_keys(self.username)#Finds the username/email info field element using its name
        self.driver.find_element(By.NAME,"pass").send_keys(self.password)#Finds the password info field element using its name
        time.sleep(2)
        self.driver.find_element(By.NAME,"login").click() #Clicks the login button
        time.sleep(7)

    def search(self,profile):
        search_bar = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div/label/input')
        search_bar.click() #Clicks the Search Bar
        search_bar.send_keys(profile)#Types the profile that you want to search
        search_bar.send_keys(Keys.ENTER)
        time.sleep(3)
        self.driver.find_element(By.LINK_TEXT,profile).click()
        time.sleep(4)
    
    def profile_interaction(self):
        photos = self.driver.find_element(By.LINK_TEXT,'photos')
        photos.click()

def data_entry(): #Function for the user input to the gui
    layout1 = [ #Default layout for the gui
        [sg.Text("Please enter your Username, Password, and an action")],
        [sg.Text("Username", key = "_Username_", size = (15,1)), sg.InputText()],
        [sg.Text("Password", key = "_Password_", size = (15,1)), sg.InputText()],
        [sg.Button("Search Account")]
    ] 
    layout2 = [ #Layout for Account Searching
        [sg.Text("Please enter your Username, Password, and Account to search")],
        [sg.Text("Username", key = "_Username_", size = (15,1)), sg.InputText()],
        [sg.Text("Password", key = "_Password_", size = (15,1)), sg.InputText()],
        [sg.Text("Search", key = "_Search_", size = (15,1)),sg.InputText()]
    ]

    layout = [[sg.Column(layout1, key = '_COL1_'),sg.Column(layout2, visible=False, key= '_COL2_')],
             [sg.Submit(),sg.Cancel(),sg.Button("Print")]]
    window = sg.Window('Login Information/Search Query', layout)
    layout = 1

    answers = []
    while True:
        event,values = window.read()
        if event == "Submit":
            username = values[0]
            password = values[1]
            answers.append(username)
            answers.append(password)
            if layout == 2:
                account = values[2]
                answers.append(account)
            window.close()
            return answers
        if event == "Search Account":
            window[f'_COL{layout}_'].update(visible=False)
            layout+=1
            window[f'_COL{layout}_'].update(visible=True)
        if event == "Print":
            for i in values:
                print(values[i])
        if event == sg.WIN_CLOSED or event == "Cancel":
            break
        

if __name__ == '__main__':
    info = data_entry()
    print("This is info[0]"+info[0])
    print("this is info[1]"+info[1])
    fb_bot = FacebookBot(info[0], info[1])
    fb_bot.search(info[2])
    fb_bot.profile_interaction()

    
