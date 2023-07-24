
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import PySimpleGUI as sg
import time
from time import sleep
import chromedriver_autoinstaller
chromedriver_autoinstaller.install() #Auto installs chromedriver based on the version of chrome installed
option1 = Options()
option1.add_argument("--disable-notifications")



class FacebookBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(options=option1)
        self.driver.maximize_window()
        self.login()

    def login(self):
        
        self.driver.get('https://www.facebook.com/') #Navigates to the facebook info page
        time.sleep(2)
        self.driver.find_element(By.NAME,"email").send_keys(self.username) #Finds the username/email info field element using its name
        self.driver.find_element(By.NAME,"pass").send_keys(self.password) #Finds the password info field element using its name
        time.sleep(2)
        self.driver.find_element(By.NAME,"login").click() #Clicks the login button


    def search(self,profile):
        try:
            w = WebDriverWait(self.driver, 15)
            w.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[1]/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div/div/label/input"))) #Waits of the search bar to be loaded
            search_bar = self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[2]/div[3]/div/div/div[1]/div/div/label/input') #Finds the search bar using its xpath
            search_bar.click() #Clicks the Search Bar
            search_bar.send_keys(profile)#Types the profile that you want to search
            search_bar.send_keys(Keys.ENTER)
            time.sleep(3)
            self.driver.find_element(By.LINK_TEXT,profile).click()
            time.sleep(4)
        except TimeoutException:
            print("Timeout occured")
    

def data_entry(): #Function for the user input to the gui
    layout1 = [ #Default layout for the gui
        [sg.Text("Please enter your Username, Password, and an action")],
        [sg.Text("Username", size = (15,1)), sg.InputText(key="_Username_")],
        [sg.Text("Password", size = (15,1)), sg.InputText(key="_Password_")],
        [sg.Button("Search Account")]
    ] 
    layout2 = [ #Layout for Account Searching
        [sg.Text("Please enter your Username, Password, and an account to search")],
        [sg.Text("Username", size = (15,1)), sg.InputText(key="_Username_S")],
        [sg.Text("Password", size = (15,1)), sg.InputText(key="_Password_S")],
        [sg.Text("Search", size = (15,1)),sg.InputText(key="_Search_")],
        [sg.Button("Back")]
    ]

    layout = [[sg.Column(layout1, key = '_COL1_'),sg.Column(layout2, visible=False, key= '_COL2_')],
             [sg.Submit(),sg.Cancel()]]
    window = sg.Window('Login Information/Search Query', layout)
    layout = 1

    answers = []
    while True:
        event,values = window.read()
        print(event,values)
        if event == "Submit":
            if layout == 1:
                username = values["_Username_"]
                password = values["_Password_"]
                answers.append(username)
                answers.append(password)
            if layout == 2:
                username = values["_Username_S"]
                password = values["_Password_S"] 
                account = values["_Search_"]
                answers.append(username)
                answers.append(password)
                answers.append(account)
            
            window.close()
            return answers
            
        if event == "Search Account":#Swaps current layout for account search layout
            window[f'_COL{layout}_'].update(visible=False)
            layout+=1
            window[f'_COL{layout}_'].update(visible=True)
        if event == "Back": #Swaps current layout for default layout
            window[f'_COL{layout}_'].update(visible=False)
            layout-=1
            window[f'_COL{layout}_'].update(visible=True)
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

    
if __name__ == '__main__':
    info = data_entry()
    if info is None: #if no informatio was entered
        print("All fields must be filled out")
        exit()
    fb_bot = FacebookBot(info[0], info[1])
    if len(info) > 2:
        fb_bot.search(info[2])

    
