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
from kivy.uix.image import Image

import math
from random import randint, choice, random

class MainMenu(Screen):
    pass

class GameScreen(Screen):
    enemy_counts = NumericProperty(0)
    def __init__(self, **kw):
        super().__init__(**kw)
        self.random_between = (20, 70)
        self.bullet_damage = 5
        
        self.enemies = dict() # Store all enemy objects
        self.all_items = dict()
        
        Clock.schedule_interval(self.update, 1/60)

    def on_wave(self, dt):
        pass

    def create_enemy(self, pos=(500, 500), speed=0 ,enemy_id=None):
        print(f'Create Enemy at {pos} and speed {speed}')
        enemy = Enemy(pos=pos, speed=speed,enemy_id=enemy_id)
        self.add_widget(enemy)
        self.enemies[enemy_id] = enemy # add dynamic enemy to list 
        
    #Give ID to enemy
    def create_multiple_enemies(self, positions, speed):
        for i, pos in enumerate(positions):
            self.create_enemy(pos=pos, speed=speed[i], enemy_id=f"Enemy_{i+1}")
       
    def update(self, dt):
        for key, enemy in self.enemies.items():
            if enemy.enable == True:
                enemy.follow_player(self.ids.player.pos, (self.ids.player.base_width, self.ids.player.base_height), dt)

                    
    def on_enter(self):
        self.ids.player.enable_keyboard()
        
        #Create multiplae enemies here
        positions = [(500, 500), (600, 400), (700, 300), (400, 600)]
        speed = [randint(self.random_between[0], self.random_between[1]) for i in range(len(positions))]
        
        self.enemy_counts = len(positions)
        
        self.create_multiple_enemies(positions, speed)
        for key ,enemy in self.enemies.items():
            enemy.enable_enemy()
        
    def on_leave(self):
        self.ids.player.disable_keyboard()
        for key, enemy in self.enemies.items():
            enemy.disable_enemy()
        
        #reset value
        # --- Player ---
        self.ids.player.pos = (50, 50)
        self.ids.player.bullet_left = 20
        self.ids.player.rotation = 0
        self.ids.player.score = 0
        # --- Enemys ---
        
        # --- Items ---
        for key, item in self.all_items.items():
            self.remove_widget(item)
        self.all_items.clear()    
        
        # Reset enemies and remove them from the screen
        for key, enemy in self.enemies.items():
            self.remove_widget(enemy)
        self.enemies.clear()  # Clear the list
        
    def minus_player_hp(self, enemy_id):
        self.ids.player.hp_left -= 1
        print(f'Enemy id {enemy_id} attack!')

        #Make Delay Enemy
        self.enemies[enemy_id].disable_enemy()
        
        Clock.schedule_once(lambda dt: self.re_enable_enemy(enemy_id), 4)

    def re_enable_enemy(self, enemy_id):
        self.enemies[enemy_id].enable_enemy()

    def minus_enemy_hp(self, enemy_id, damage):
        if self.enemies[enemy_id].hp_left != 0:
            self.enemies[enemy_id].hp_left -= damage
            print(f'subtract enemy {enemy_id} | HP left = {self.enemies[enemy_id].hp_left}')
            if self.enemies[enemy_id].hp_left <= 0:
                self.enemies[enemy_id].disable_enemy()

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
    def __init__(self, x, y, rotation, damage, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        self.rotation = rotation
        self.velocity = 500  # Speed
        self.damage = damage

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
    
        #Check Collide with Enemy??
        for key, enemy in self.parent.enemies.items():
            if self.collide_with_enemy(enemy.pos, (enemy.base_width, enemy.base_height)) == True:
                self.parent.minus_enemy_hp(enemy.enemy_id, self.damage) # cal fn() 
                self.remove_bullet()
        
        #Check Collind with wall
        if self.x < 42 or self.x > Window.width-42 or self.y < 42 or self.y > Window.height-42: # 42 mean pixel of width and height of wall in background
            self.remove_bullet()
        

    # True False
    def collide_with_enemy(self, enemy_pos, enemy_size):
        r1x = self.x
        r1y = self.y
        r2x = enemy_pos[0]
        r2y = enemy_pos[1]
        r1w = self.base_width
        r1h = self.base_height
        r2w = enemy_size[0]
        r2h = enemy_size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False


    def remove_bullet(self):
        if self.parent:
            self.parent.remove_widget(self)
        
        Clock.unschedule(self.move_bullet)

class Enemy(Widget):
    rotation = NumericProperty(0)
    hp_left = NumericProperty(5)
    
    def __init__(self, speed,enemy_id=None, **kwargs):
        super().__init__(**kwargs)
        #Property
        self.speed = speed
        self.enemy_id = enemy_id
        self.enable = False
        self.get_player = False

        Clock.schedule_interval(self.debug_values, 1/60) #Check Frame by Frame

    def debug_values(self, dt):
        #Check Enemy hp
        if self.hp_left < 0:
            self.hp_left = 0

    def enable_enemy(self):
        self.enable = True
        print(f'Enable enemy! {self.enemy_id}')
        
    def disable_enemy(self):
        self.enable = False
        print(f'Disable enemy! {self.enemy_id}')
        
        #Check On enemy died
        if self.hp_left <= 0:
            self.parent.ids.player.score += 100 #add score
            self.parent.enemy_counts -= 1 #subtractenemy left
            if random() < 0.5: #random 50%
                self.spawn_item(self.pos, self.enemy_id)
            self.pos = (-50, -50)
    
    def follow_player(self, player_pos, player_size, dt):
        # cal angle between player and enemy
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        angle = math.atan2(dy, dx)  # cal rotation of enemy
        self.rotation = math.degrees(angle)

        step_size = self.speed * dt
        move_x = step_size * math.cos(angle)  # move X
        move_y = step_size * math.sin(angle)  # move Y

        # Update position enemy
        new_pos = (self.pos[0] + move_x, self.pos[1] + move_y)
        #Check
        if self.collide_with_player(new_pos, player_pos, player_size) == False:
            self.pos = new_pos #Update
        else:
            self.attack_player()
            
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
            self.get_player = True
            return True
        else:
            self.get_player = False
            return False
        
    def attack_player(self):
        if self.get_player == False:  # debug 
            return
        self.parent.minus_player_hp(self.enemy_id)  # call fn() in GameScreen

    def spawn_item(self, pos, item_id):
        if item_id in self.parent.all_items:
            print(f"Item ID {item_id} already exists. Skipping spawn.")
            return  # ป้องกันการสร้าง item ที่มี id ซ้ำ
        
        item_type = choice(['h', 'a'])
        if item_type == 'h':
            widget = Heal_item(pos=pos, item_id=item_id)
        elif item_type == 'a':
            widget = Ammo_item(pos=pos, item_id=item_id)

        self.parent.all_items[item_id] = widget  # เก็บ widget ลงใน dictionary
        self.parent.add_widget(widget)  # เพิ่ม widget ลงในหน้าจอ
        print(f"Spawned {item_type} item with ID {item_id} at {pos}")


class Player(Widget):
    rotation = NumericProperty(0)
    bullet_left = NumericProperty(20)
    hp_left = NumericProperty(1000)
    score = NumericProperty(0)
    heal_item_left = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)     
        #Property
        self.gun_type = "shotgun"
        self.pos = (50, 50)
    
        self.keysPressed = set()
        self._keyboard = None
            
        Clock.schedule_interval(self.move_step, 1/60)
        Clock.schedule_interval(self.check_collide_item, 1/60)
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
                
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def shoot_bullet(self):
        bullet = Bullet(self.pos[0]+self.base_width/2, self.pos[1]+self.base_height/2, self.rotation, self.parent.bullet_damage)
        self.parent.add_widget(bullet)  # add bullet to screen
        #Check gun type
        if self.gun_type == "shotgun":
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
        if "1" in self.keysPressed:
            self.gun_select("shotgun")
        if "2" in self.keysPressed:
            self.gun_select("pistol")

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
        #Check Player hp
        if self.hp_left > 200:
            self.hp_left = 200
        if self.hp_left < 0:
            self.hp_left = 0
        #Check Bullet Left
        if self.bullet_left > 99:
            self.bullet_left = 99
        if self.bullet_left < 0:
            self.bullet_left = 0
        #Check heal item left
        if self.heal_item_left > 99:
            self.heal_item_left < 99
        if self.heal_item_left < 0:
            self.heal_item_left = 0
    
    
    def gun_select(self, gun):
        if gun == "shotgun":
            self.gun_type = gun
            self.parent.bullet_damage = 5
            #make parent ui move
            self.parent.ids.select_line.pos_hint = {'center_x': 62.5/1280, 'center_y': 0.065}
        elif gun == "pistol":
            self.gun_type = gun
            self.parent.bullet_damage = 0.5

            self.parent.ids.select_line.pos_hint = {'center_x': (62.5+94)/1280, 'center_y': 0.065}

    def check_collide_item(self, dt): #update
        for key, item in list(self.parent.all_items.items()):
            r1x = self.x
            r1y = self.y
            r2x = item.x
            r2y = item.y
            r1w = self.base_width
            r1h = self.base_height
            r2w = item.base_width
            r2h = item.base_height

            if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
                item.add_to_player(self)
    
class Heal_item(Widget):
    def __init__(self, item_id,**kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id

    def add_to_player(self, player):
        player.heal_item_left += 1
        self.del_item()
        
    def del_item(self):
        del self.parent.all_items[self.item_id] # del self in game items dict
        self.parent.remove_widget(self)
        
class Ammo_item(Widget):
    def __init__(self, item_id,**kwargs):
        super().__init__(**kwargs)
        self.item_id = item_id
    
    def add_to_player(self, player):
        player.bullet_left += 1
        self.del_item()

    def del_item(self):
        del self.parent.all_items[self.item_id] # del self in game items dict
        self.parent.remove_widget(self)

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
