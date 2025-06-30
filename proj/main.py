from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.text import LabelBase
from kivy.lang import Builder

# Register custom font
LabelBase.register(name="Orbitron", fn_regular="Orbitron/static/Orbitron-Medium.ttf")

class MenuScreen(Screen):
    pass

class HighScoreScreen(Screen):
    pass

class SpeedScreen(Screen):
    pass

class ThanksScreen(Screen):
    pass

class LanguageScreen(Screen):
    pass

class ScrollingScreen(Screen):
    pass

class GameScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        return Builder.load_file("main.kv")

if __name__ == "__main__":
    MyApp().run()
