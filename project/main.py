import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window


# Main Menu
class MainMenu(Screen):
    pass

# In Game
class GameScreen(Screen):
    pass

#Player
class Player(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #Keyboard
        self._keyboard = Window.request_keyboard(self, self._on_keyboard_closed)
        self._keyboard.bind(on_key_down=self._on_key_down)
    
#on keyboard input
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('Keyboard Detected')
        print(self.pos)
        currentx, currenty = self.pos
        
        if text == "w":
            currenty += 1
        if text == "s" :
            currenty -= 1
        if text == "a":
            currentx -= 1
        if text == "d":
            currentx += 1
            
        self.pos = (currentx, currenty)
        


# Main App
class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()
