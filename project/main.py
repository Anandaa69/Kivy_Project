import kivy
kivy.require('2.3.1')

from kivy.config import Config

# กำหนดค่าคอนฟิก
Config.set('graphics', 'width', '1280')  # ความกว้างของหน้าต่าง
Config.set('graphics', 'height', '720')  # ความสูงของหน้าต่าง
Config.set('graphics', 'resizable', False)  # ปิดการปรับขนาดหน้าต่าง

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty

# Main Menu
class MainMenu(Screen):
    pass

# In Game
class GameScreen(Screen):
    def on_enter(self):
        pass
    
    def on_leave(self): 
        self.ids.player.pos = (0, 0)

class SettingScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.select = 0 # 0 --> 1280 , 1 --> 1980

    def select_screen(self, value):
        if value == 0:
            print('Change to 1280x720')
            Window.fullscreen = False
            Window.size = (1280, 720)
        elif value == 1:
            print('Change to FullScreen')
            Window.fullscreen = True

#Player
class Player(Widget):
    rotation = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        #Keyboard
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
    
        self.keysPressed = set()

        self.center_player = list()
        
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
        
        #Setup
        step_size = 100 * dt
        step_rotate = 190 * dt
        
        if "w" in self.keysPressed:
            currenty += step_size
        if "s" in self.keysPressed :
            currenty -= step_size
        if "a" in self.keysPressed:
            currentx -= step_size
        if "d" in self.keysPressed:
            currentx += step_size
        
        if "j" in self.keysPressed:
            self.rotation += step_rotate
        if "k" in self.keysPressed:
            self.rotation -= step_rotate
        if "l" in self.keysPressed:
            print(self.center)
            print('pos =',self.pos)
            print('size =',self.size)
        #Update
        self.pos = (currentx, currenty)

# Main App
class MyGameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name='main_menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingScreen(name='setting_menu'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()
