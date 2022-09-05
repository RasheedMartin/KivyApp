import glob
from datetime import datetime # Used to get the system time
import random

from kivy.core.text import Label
from kivy.uix.popup import Popup

from hoverable import HoverBehavior #Hovering effecton logout button
from kivy.app import App # strt of the app
from kivy.uix.screenmanager import *
from kivy.lang import Builder
import json
from pathlib import Path
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior

# class Grid_Layout_Demo(GridLayout):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.cols = 2
#
#         self.l1 = Label(
#             text="User Login"
#         )
#         self.add_widget(self.l1)
#
#         self.b1 = Button(text="Click Me", background_color=(0,24,67,1))
#         self.add_widget(self.b1)

#
# class DemoApp(App):
#     def build(self):
#         return Grid_Layout_Demo()
#
#
# DemoApp().run()

Builder.load_file('design.kv')


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current = "signup_screen"
        self.manager.transition.direction = 'left'

    def login(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:
            self.manager.current = "login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"


class RootWidget(ScreenManager):
    pass


class SignUpScreen(Screen):
    def back(self):
        self.manager.current = "Login_screen"
        self.manager.transition.direction = 'right'

    def add_user(self, uname, pword):
        with open("users.json") as file:
            users = json.load(file)

        users[uname] = {'username': uname, 'password': pword, 'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open("users.json", 'w') as file:
            json.dump(users, file)

        self.manager.current = 'sign_up_screen_success'


class SignUpScreenSuccess(Screen):
    def login(self):
        self.manager.current = "Login_screen"
        self.manager.transition.direction = 'right'


class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "Login_screen"


    def get_quote(self, feel):
        feel = feel.lower()
        available_feelings = glob.glob("quotes//*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if feel in available_feelings:
            with open(f"quotes//{feel}.txt", encoding="utf8") as file:
                quotes = file.readlines()
            self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling"


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class MainApp(App):
    def build(self):
        return RootWidget()


if __name__ == "__main__":
    MainApp().run()