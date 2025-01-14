import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen

# Main Menu
class MainMenu(Screen):
    pass

# In Game
class GameScreen(Screen):
    pass

# Main App
class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()
