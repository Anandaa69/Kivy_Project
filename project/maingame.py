import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Main Menu Game!
class MainMenu(BoxLayout):
    #On press botton --> clear widgets add start game
    def start_game(self):
        app = App.get_running_app()
        app.root.clear_widgets()
        app.root.add_widget(Label(text="Game Started!", font_size=24))
class MyGameApp(App):
    def build(self):
        return MainMenu()
    
if __name__ == '__main__':
    MyGameApp().run()
