import kivy
kivy.require('2.3.1')

from kivy.config import Config

# Screen Config
Config.set('graphics', 'width', '1280')  # Width of Screen
Config.set('graphics', 'height', '720')  # Height of Screen
Config.set('graphics', 'resizable', False)  # Set can't change screen size

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics import Ellipse, Line
import math

class MainMenu(Screen):
    pass

class GameScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        Clock.schedule_interval(self.update, 1/60)
    
    def update(self, dt):
        if self.ids.E_1.enable == True:
            self.ids.E_1.follow_player(self.ids.player.pos, (self.ids.player.base_width, self.ids.player.base_height), dt)
        
    def on_enter(self):
        self.ids.player.enable_keyboard()
        self.ids.E_1.enable_enemy()
        
    def on_leave(self):
        self.ids.player.disable_keyboard()
        self.ids.E_1.disable_enemy()
        
        #reset value
        # --- Player ---
        self.ids.player.pos = (50, 50)
        self.ids.player.bullet_left = 20
        self.ids.player.rotation = 0
        # -- Enemy ---
        self.ids.E_1.pos = (500, 500)
        
class SettingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.select = 0 # 0 --> 1280 , 1 --> 1980

    def select_screen(self, value):
        if value == 0:
            print('Change to 1280x720')
            Window.fullscreen = False
            Window.size = (1280, 720)
        elif value == 1:
            print('Change to FullScreen')
            Window.fullscreen = True

class Bullet(Widget):
    def __init__(self, x, y, rotation, **kwargs):
        super().__init__(**kwargs)
        self.size = (10, 10)
        self.pos = (x, y)
        self.rotation = rotation
        self.velocity = 500  # Speed

        # Update frame by frame
        Clock.schedule_interval(self.move_bullet, 1/60)

    def move_bullet(self, dt):
        # Bullet path cal
        angle_rad = math.radians(self.rotation)

        dx = self.velocity * dt * math.cos(angle_rad)
        dy = self.velocity * dt * math.sin(angle_rad)

        # Update values
        self.x += dx
        self.y += dy
        self.pos = (self.x, self.y)

        #Check Collide with Wall
        if self.x < 42 or self.x > Window.width-42 or self.y < 42 or self.y > Window.height-42: # 42 mean pixel of width and height of wall in background
            self.remove_bullet()
        
    def remove_bullet(self):
        if self.parent:
            self.parent.remove_widget(self)
        
        Clock.unschedule(self.move_bullet)

class Enemy(Widget):
    rotation = NumericProperty(0)
    health_enemy_left = NumericProperty(5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos = 500, 500
        self.enable = False
        
    def enable_enemy(self):
        self.enable = True
        print('Enable enemy!')
        
    def disable_enemy(self):
        self.enable = False
        print('Eisable enemy!')
    
    def follow_player(self, player_pos, player_size, dt):
        # cal angle between player and enemy
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        angle = math.atan2(dy, dx)  # cal rotation of enemy
        self.rotation = math.degrees(angle)

        step_size = 100 * dt
        move_x = step_size * math.cos(angle)  # move X
        move_y = step_size * math.sin(angle)  # move Y

        # Update position enemy
        new_pos = (self.pos[0] + move_x, self.pos[1] + move_y)
        #Check
        if self.collide_with_player(new_pos, player_pos, player_size) == False:
            self.pos = new_pos #Update

    def collide_with_player(self, new_pos, player_pos, player_size):
        r1x = new_pos[0]
        r1y = new_pos[1]
        r2x = player_pos[0]
        r2y = player_pos[1]
        r1w = self.base_width
        r1h = self.base_height
        r2w = player_size[0]
        r2h = player_size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            print('You has been Attack!!')
            return True
        else:
            return False
        
        return False
        
    def attack_player(self):
        pass

class Player(Widget):
    rotation = NumericProperty(0)
    bullet_left = NumericProperty(20)
    health_left = NumericProperty(5)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)     
        #Property
        self.pos = (50, 50)
    
        self.keysPressed = set()
        self._keyboard = None
            
        Clock.schedule_interval(self.move_step, 1/60)
        Clock.schedule_interval(self.debug_values, 1/60)

    def enable_keyboard(self):
        if not self._keyboard:
            self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_key_down)
            self._keyboard.bind(on_key_up=self._on_key_up)
            print('Enable Player!')
            
    def disable_keyboard(self):
        if self._keyboard:
            self._keyboard.unbind(on_key_down=self._on_key_down)
            self._keyboard.unbind(on_key_up=self._on_key_up)
            self._keyboard = None
            
            #set to None
            self.keysPressed = set()
            
            print('Disable Player!')

    def _on_keyboard_closed(self): 
        self.disable_keyboard()
        
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(text)

        if text == " ":  # press SpcaeBar to shoot
            if self.bullet_left > 0:
                self.shoot_bullet()
                print(self.bullet_left)
            else:
                print('Out of Bullet!') 
                
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def shoot_bullet(self):
        bullet = Bullet(self.pos[0]+self.base_width/2, self.pos[1]+self.base_height/2, self.rotation)
        self.parent.add_widget(bullet)  # add bullet to screen
        self.bullet_left -= 1

    def move_step(self, dt):
        currentx, currenty = self.pos
        
        #Setup
        step_size = 300 * dt
        step_rotate = 150 * dt
        
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
        #Check
        if "l" in self.keysPressed:
            print(self.rotation)
            print('pos =',self.pos)
            print('size =',self.size)
        if "i" in self.keysPressed:
            print(self.bullets)
        
        #Check Collide?
        new_pos = (currentx, currenty)
        if self.collide_with_wall(new_pos) == False:
            self.pos = new_pos #Update

    def collide_with_wall(self, new_pos):
        x, y = new_pos
        if x < 42 or x + self.base_width > Window.width - 42:
            return True
        if y < 42 or y + self.base_height > Window.height - 42:
            return True
        
        return False

    def debug_values(self, dt):
        #Check Player Health
        if self.health_left > 99:
            self.health_left = 99
        if self.health_left < 0:
            self.health_left = 0
        #Check Bullet Left
        if self.bullet_left > 99:
            self.bullet_left = 99
        if self.bullet_left < 0:
            self.bullet_left = 0
        
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
