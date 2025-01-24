import kivy
from kivy.config import Config
kivy.require('2.3.1')

# Screen Config
Config.set('graphics', 'width', '1280')  # Width of Screen
Config.set('graphics', 'height', '720')  # Height of Screen
Config.set('graphics', 'resizable', False)  # Set can't change screen size
Config.set('graphics', 'maxfps', '60')  # Set FPS to 144 fps

from kivy.core.window import Window
# Window.fullscreen = True

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty
from kivy.graphics import Ellipse, Line, Rotate, PushMatrix, PopMatrix
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.core.audio import SoundLoader
import math
from random import randint, choice, random

class MainMenu(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bg_song = None

        Clock.schedule_interval(self.update, 1/60)
        
    def on_enter(self):
        self.bg_song = SoundLoader.load('assets/sounds/main_bg.mp3')
        if self.bg_song:
            self.bg_song.loop = True
            self.bg_song.volume = self.ids.bg_s.value/100
            self.bg_song.play()
            
    def update(self, dt):
        #Check Slider
        self.bg_song.volume = self.ids.bg_s.value/100

    def sound_test(self):
        sfx = SoundLoader.load('assets/sounds/shotgun.mp3')
        if sfx:
            sfx.volume = self.ids.sound_ef.value/100
            sfx.play()
        
    def on_leave(self):
        self.bg_song.stop()
        
        game_screen = self.manager.get_screen('game')
        game_screen.update_volume(self.ids.bg_s.value/100, self.ids.sound_ef.value/100)
    
class EndGame(Screen):
    total_score = NumericProperty(0)
    wave = NumericProperty(0)

    def update_score(self, score):
        self.total_score = score

    def update_wave(self, wave):
        self.wave = wave
    
class GameScreen(Screen):
    enemy_counts = NumericProperty(0)
    wave_game = NumericProperty(0)
    
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bullet_damage = 5
        #Sound
        self.sfx_volume = 0
        self.bg_volume = 0
        self.all_sfx = []
        
        self.enemy_damage = 10
        self.random_between = (20, 70)
        self.enemies_now = 10
        self.enemies_max = 150
        
        #add by next wave
        self.enemy_nw_add = 3
        
        self.end_wave_tick = 0
        self.all_obstacles = list() # Store all obstacles object
        self.enemies = dict() # Store all enemy objects
        self.all_items = dict()
        
        Clock.schedule_interval(self.update, 1/60)

    def create_enemy(self, dt):
        random_spawn = [self.ids.spawn_1, self.ids.spawn_2, self.ids.spawn_3, self.ids.spawn_4, self.ids.spawn_5]
        for i in range(self.enemies_now):
            pos = choice(random_spawn).pos
            pos[0] += choice(range(30))
            enemy = Enemy(pos=pos, speed=randint(self.random_between[0], self.random_between[1]), enemy_id=str(i+1))
            self.add_widget(enemy)
            self.enemies[str(i+1)] = enemy # add dynamic enemy to list 
            enemy.enable_enemy() # Enemy on!
            # self.enemy_counts += 1
        self.next_game_value()
    
    def create_obstacle(self, positions, images):
        for i, pos in enumerate(positions):
            obstacle = Obstacle(pos=pos, size_hint=(None, None), source=images[i])
            self.add_widget(obstacle, index=-1)
            self.all_obstacles.append(obstacle)
            
    def update(self, dt):
        for key, enemy in self.enemies.items():
            if enemy.enable == True:
                enemy.follow_player(self.ids.player.pos, (self.ids.player.base_width, self.ids.player.base_height), dt)
        self.end_wave()
        # print(f'sfx === {self.sfx_volume}')
        # print(f'bg === {self.bg_volume}')
        
    def on_enter(self):
        self.ids.player.enable_keyboard()
        
        #Create Obstacles here
        obstacle_positions = [(310, 131), (310, 392), (570, 131), (830, 131), (830, 392), (42, 150), (1050, 520), (570, 400)] 
        obstacle_images = ['assets/obstacle.png' for _ in range(5)] + ['assets/obstacle_2.png', 'assets/obstacle_4.png', 'assets/obstacle.png']
        
        self.create_obstacle(obstacle_positions, obstacle_images)
        
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
        self.ids.player.hp_left = self.ids.player.hp_max
        self.ids.player.heal_item_left = 0
        self.ids.player.coin = 0
        self.ids.player.speed = 100
        self.ids.player.hp_left = 100
        self.ids.player.hp_max = 100
        
        # --- Enemys ---
        self.enemy_counts = 0
        # --- Items ---
        for key, item in self.all_items.items():
            self.remove_widget(item)
        self.all_items.clear()    
        
        #reset value game
        self.enemy_damage = 10
        self.random_between = (20, 70)
        self.enemies_now = 10
        self.enemies_max = 100
        self.speed_max = 100
        self.wave_game = 0
        
        # Reset enemies and remove them from the screen
        for key, enemy in self.enemies.items():
            self.remove_widget(enemy)
        self.enemies.clear()  # Clear the list
        
    def minus_player_hp(self, enemy_id):
        self.ids.player.hp_left -= self.enemy_damage
        print(f'Enemy id {enemy_id} attack!')

        #Make Delay Enemy
        self.enemies[enemy_id].disable_enemy()
        Clock.schedule_once(lambda dt: self.re_enable_enemy(enemy_id), 4)

    def re_enable_enemy(self, enemy_id):
        if enemy_id in self.enemies:
            self.enemies[enemy_id].enable_enemy()

    def minus_enemy_hp(self, enemy_id, damage):
        if self.enemies[enemy_id].hp_left != 0:
            self.enemies[enemy_id].hp_left -= damage
            print(f'subtract enemy {enemy_id} | HP left = {self.enemies[enemy_id].hp_left}')
            if self.enemies[enemy_id].hp_left <= 0:
                self.enemies[enemy_id].disable_enemy()
                self.remove_widget(self.enemies[enemy_id]) #remove this enemy from game !
                del self.enemies[enemy_id] # remove this enemy from dict!

    def end_wave(self):
        #On end wave show store
        if self.enemy_counts == 0:
            self.ids.store.opacity = 1
        else:
            self.ids.store.opacity = 0
        
        check = self.ids.player.collide_with(self.ids.player.pos, self.ids.nw_ob.pos, self.ids.nw_ob.size)
        if self.enemy_counts != 0 and check == True or check == False:
            self.ids.bt_nw.disabled = True
            self.ids.bt_nw.opacity = 0
            
        elif check == True and self.enemy_counts == 0:
            self.ids.bt_nw.disabled = False
            self.ids.bt_nw.opacity = 1
            
        check_2 = self.ids.player.collide_with(self.ids.player.pos, self.ids.store.pos, self.ids.store.size)
        if self.enemy_counts != 0 and check_2 == True or check_2 == False:
            self.ids.bt_store.disabled = True
            self.ids.bt_store.opacity = 0
        elif check_2 == True and self.enemy_counts == 0:
            self.ids.bt_store.disabled = False
            self.ids.bt_store.opacity = 1  
            
    def next_wave(self):
        # self.delay_time = 1 # check!!!!!!
        # self.ids.bt_nw.disabled = True
        self.wave_game += 1
        self.enemy_counts = self.enemies_now
        Clock.schedule_once(self.create_enemy, 3)
        
        wave_label = WaveLabel(f'WAVE {self.wave_game}')
        self.add_widget(wave_label)  # เพิ่ม WaveLabel เข้าไปใน GameScreen
        wave_label.show_message(duration=0.5)

    def show_upgrade_popup(self):
        # สร้างและเปิด Popup
        popup = UpgradePopup(self)
        popup.open()
    
    def next_game_value(self):
        #give harder to game
        if self.enemies_now <= self.enemies_max:
            self.enemies_now += self.enemy_nw_add #add 5 enemy to next wave
        self.enemy_damage += 5 #add 5 enemy damage
        self.random_between = [x + 10 for x in self.random_between] 
        # print(f'REPORT NEXT WAVE is {self.wave_game}')
        # print(f'speed = {self.random_between}')
        # print(f'enemy damage = {self.enemy_damage}')
        # print(f'enemy count = {self.enemies_now}')      

    def end_game(self):
        # send score and wave to end screen
        end_screen = self.manager.get_screen('end_game')
        end_screen.update_score(self.ids.player.score)
        end_screen.update_wave(self.wave_game)
        # change to end screen
        self.manager.current = 'end_game'

    def update_volume(self, bg_volume, sfx_volume):
        self.sfx_volume = sfx_volume
        self.bg_volume = bg_volume

# class Sound(SoundLoader):
#     def __init__(self) -> None:
#         super().__init__()

class UpgradePopup(Popup):
    coin = NumericProperty(0)
    def __init__(self, game_screen, **kwargs):
        super().__init__(**kwargs)
        self.game_screen = game_screen  # รับ GameScreen เพื่อให้สามารถเข้าถึงตัวแปรต่างๆ
        self.coin = game_screen.ids.player.coin
        self.price = 20
        self.price_2 = 10
        if self.game_screen:
            self.game_screen.ids.player.bind(coin=self.update_coin)
    
    def update_coin(self, instance, value):
        self.coin = value  # Update the coin in UpgradePopup when it changes
    
    def upgrade_speed(self):
        if self.game_screen.ids.player.coin > 0 and self.game_screen.ids.player.coin - self.price >= 0:
            self.game_screen.ids.player.speed += 10
            print(self.game_screen.ids.player.speed)
            
            self.game_screen.ids.player.coin -= self.price
            print('UPGRADE SPEED!!!')
        else:
            print('Cant buy')

    def upgrade_hp(self):
        if self.game_screen.ids.player.coin > 0 and self.game_screen.ids.player.coin - self.price >= 0:
            self.game_screen.ids.player.hp_left += 5
            self.game_screen.ids.player.hp_max += 5
            
            self.game_screen.ids.player.coin -= self.price
            print('UPGRADE HP!!!')
        else:
            print('Cant buy')

    def buy_bullet(self):
        if self.game_screen.ids.player.coin > 0 and self.game_screen.ids.player.coin - self.price_2 >= 0:
            self.game_screen.ids.player.bullet_left += 1
            self.game_screen.ids.player.coin -= self.price_2

    def buy_heal(self):
        if self.game_screen.ids.player.coin > 0 and self.game_screen.ids.player.coin - self.price_2 >= 0:
            self.game_screen.ids.player.heal_item_left += 1
            self.game_screen.ids.player.coin -= self.price_2
            
class WaveLabel(Widget):
    def __init__(self, wave, **kwargs):
        super().__init__(**kwargs)
        self.wave = wave
        self.label = Label(
            text=wave,
            font_size="70sp",
            opacity=0,  
            size_hint=(None, None),  
            size=(800, 200),
            halign="center",
            valign="middle",
        )
        self.add_widget(self.label)

    def on_parent(self, instance, parent):
        if parent:
            self.label.center_x = parent.center_x 
            self.label.center_y = parent.top * 0.85

    def show_message(self, duration=2):
        # Animation: เพิ่ม opacity เป็น 1
        fade_in = Animation(opacity=1, duration=duration / 0.5)
        # Animation: ลด opacity กลับไปเป็น 0
        fade_out = Animation(opacity=0, duration=duration / 0.5)

        # รวม Animation (fade_in -> fade_out)
        fade_in += fade_out
        fade_in.bind(on_complete=self.remove_widget_from_parent)  # ลบตัวเองเมื่อ Animation เสร็จ
        fade_in.start(self.label)

    def remove_widget_from_parent(self, *args):
        if self.parent:
            self.parent.remove_widget(self)

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

class Obstacle(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (self.texture_size)

class Bullet(Widget):
    def __init__(self, x, y, rotation, damage, **kwargs):
        super().__init__(**kwargs)
        self.pos = (x, y)
        self.rotation = rotation
        self.velocity = 800  # Speed
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
    
        #Check Collide with Enemy?
        for key, enemy in list(self.parent.enemies.items()):
            if self.collide_with_enemy(enemy.pos, (enemy.base_width, enemy.base_height)) == True:
                self.parent.minus_enemy_hp(enemy.enemy_id, self.damage) # cal fn()
                self.remove_bullet()
                break

        
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
        
        self.last_safe_angle = None  # เพิ่มตัวแปรจดจำมุมปลอดภัยล่าสุด
        self.stuck_counter = 0  # ตัวแปรตรวจจับการติดขัด
        self.stuck_limit = 10  # จำนวนครั้งที่อนุญาตให้ติดขัดก่อนหยุดชั่วคราว
        
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
            self.parent.ids.player.coin += 10
            
            if random() < 0.5: #random 50%
                self.spawn_item(self.pos, self.enemy_id)
            self.pos = (-50, -50)
   
    def collide_with_obstacle(self):
        for obstacle in self.parent.all_obstacles:
            if self.collide_with(self.pos, obstacle.pos, obstacle.size):
                return True
        return False

    #Chat GPT GG!
    def find_clear_path(self, angle):
        step_angle = 15
        max_steps = 360 // step_angle
        found_angle = None

        for step in range(1, max_steps + 1):
            for direction in [-1, 1]:
                new_angle = angle + math.radians(direction * step * step_angle)
                move_x = self.speed * math.cos(new_angle)
                move_y = self.speed * math.sin(new_angle)
                new_pos = (self.pos[0] + move_x, self.pos[1] + move_y)

                # ตรวจสอบตำแหน่งใหม่
                if not any(self.collide_with(new_pos, obs.pos, obs.size) for obs in self.parent.all_obstacles):
                    found_angle = new_angle
                    break
            if found_angle:
                break

        if found_angle is not None:
            self.last_safe_angle = found_angle  # บันทึกมุมปลอดภัยล่าสุด
            return found_angle
        elif self.last_safe_angle is not None:
            return self.last_safe_angle  # ใช้มุมปลอดภัยล่าสุด
        else:
            return angle  # ถ้าไม่มีมุมไหนปลอดภัย ใช้มุมเดิม

    def follow_player(self, player_pos, player_size, dt):
        dx = player_pos[0] - self.pos[0]
        dy = player_pos[1] - self.pos[1]
        distance_to_player = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)

        if self.collide_with_obstacle():
            # เมื่อชน Obstacle ให้หามุมใหม่โดยใช้ find_clear_path
            if distance_to_player < 50:  # ถ้าผู้เล่นอยู่ใกล้มาก
                self.rotation = math.degrees(angle)  # หันหน้าไปหาผู้เล่น แต่ไม่ขยับ
                return
            else:
                angle = self.find_clear_path(angle)  # หาเส้นทางใหม่
                self.rotation = math.degrees(angle)
        else:
            # เมื่อไม่ชน Obstacle ให้หันไปหาผู้เล่นโดยตรง
            self.rotation = math.degrees(angle)

        # คำนวณการเคลื่อนที่
        step_size = self.speed * dt
        move_x = step_size * math.cos(angle)
        move_y = step_size * math.sin(angle)
        new_pos = (self.pos[0] + move_x, self.pos[1] + move_y)

        # ตรวจสอบการชน Player หรือกำแพง
        if not self.collide_with(new_pos, player_pos, player_size) and not self.collide_with_wall(new_pos):
            self.get_player = False
            self.pos = new_pos
        else:
            self.get_player = True
            self.attack_player()

        
    def collide_with(self, o1_pos, o2_pos, o2_size):
        r1x = o1_pos[0]
        r1y = o1_pos[1]
        r2x = o2_pos[0]
        r2y = o2_pos[1]
        r1w = self.base_width
        r1h = self.base_height
        r2w = o2_size[0]
        r2h = o2_size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False
            
    def collide_with_wall(self, new_pos):
        x, y = new_pos
        if x < 42 or x + self.base_width > Window.width - 42:
            return True
        if y < 42 or y + self.base_height > Window.height - 42:
            return True
        
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
    hp_left = NumericProperty(200)
    score = NumericProperty(0)
    heal_item_left = NumericProperty(0)
    coin = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)     
        #Property
        self.gun_type = "shotgun"
        self.pos = (50, 50)
        self.hp_max = 100
        self.heal_size = 20 # effect of heal item
        self.speed = 300
        
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
            if self.bullet_left > 0 and self.gun_type == 'shotgun':
                self.shoot_bullet()
            if self.gun_type == 'pistol':
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
            
            gun_sound = SoundLoader.load('assets/sounds/shotgun.mp3')
            if gun_sound:
                gun_sound.volume = self.parent.sfx_volume
                gun_sound.play()
            
        if self.gun_type == "pistol":
            pistol_gun = SoundLoader.load('assets/sounds/pistol.mp3')
            if pistol_gun:
                pistol_gun.volume = self.parent.sfx_volume
                pistol_gun.play()
        
    def move_step(self, dt):
        currentx, currenty = self.pos
        
        #Setup
        step_size = self.speed * dt
        step_rotate = 125 * dt
        
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
        if "h" in self.keysPressed:
            self.use_heal_item()    
            
        #Check
        if "1" in self.keysPressed:
            self.gun_select("shotgun")
        if "2" in self.keysPressed:
            self.gun_select("pistol")

        #Check Collide?
        new_pos = (currentx, currenty)
        if not any(self.collide_with(new_pos, x.pos, x.size) for x in self.parent.all_obstacles):
                if self.collide_with_wall(new_pos) == False:
                    self.pos = new_pos

    def collide_with_wall(self, new_pos):
        x, y = new_pos
        if x < 42 or x + self.base_width > Window.width - 42:
            return True
        if y < 42 or y + self.base_height > Window.height - 42:
            return True
        
        return False

    def collide_with(self, o1_pos, o2_pos, o2_size):
        r1x = o1_pos[0]
        r1y = o1_pos[1]
        r2x = o2_pos[0]
        r2y = o2_pos[1]
        r1w = self.base_width
        r1h = self.base_height
        r2w = o2_size[0]
        r2h = o2_size[1]

        if (r1x < r2x + r2w and r1x + r1w > r2x and r1y < r2y + r2h and r1y + r1h > r2y):
            return True
        else:
            return False

    def debug_values(self, dt):
        #Check Player hp
        if self.hp_left > self.hp_max:
            self.hp_left = self.hp_max
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
        #Check END GAME
        if self.hp_left == 0:
            self.parent.end_game()

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

    def use_heal_item(self):
        if self.heal_item_left > 0 and self.hp_left < self.hp_max:
            print('Use Heal Item!')
            self.heal_item_left -= 1
            self.hp_left += 20

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
        sm.add_widget(EndGame(name='end_game'))
        return sm

if __name__ == '__main__':
    MyGameApp().run()
