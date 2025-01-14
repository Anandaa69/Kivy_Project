import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock

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
        self._keyboard.bind(on_key_up=self._on_key_up)
    
        self.keysPressed = set()

        Clock.schedule_interval(self.move_step, 1/60)
#on keyboard input
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)
    
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def move_step(self, dt):
        currentx, currenty = self.pos
        
        step_size = 100 * dt
        if "w" in self.keysPressed:
            currenty += step_size
        if "s" in self.keysPressed :
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
            
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
