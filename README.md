# Watch Out! Engineer
 เป็นเกมแนว **shooting** มุมมอง **bird eyes view** ที่ผู้เล่นต้องต่อสู้กับซอมบี้ โดยผู้เล่นต้องบริหารทรัพยากรอย่าง พลังชีวิต ยา กระสุน ให้ดี โดยจุดประสงค์ของเกมต้องจัดการซอมบี้ในแต่ละ WAVE ไปเรื่อยๆจนกว่าเราจะไม่ไหว โดยในแต่ละ WAVE นั้นซอมบี้ความเก่งจะเพิ่มขึ้น
## การรันและภาพรวมของโปรแกรม
 เมื่อเข้าสู่โปรแกรมจะอยู่ที่หน้าหลักของเกม โดยในหน้าหลักจะสามารถปรับตั้งค่าเสียงได้ โดยมีให้ปรับ 2 แบบคือ Music และ SFX โดยเสียง SFX จะสามารถกดเพื่อทดสอบเสียงเอฟเฟคได้ และจะมีอยู่ 2 ปุ่มกดคือ Play และ Exit เมื่อเรากดเล่น (Play) จะทำการเข้าสู่หน้าเกม โดยผู้เล่นสามารถใช้ปุ่ม **W, A, S, D** ในการเดิน **J, K** เพื่อนหมุนซ้ายขวา กด **H** เพื่อรักษา (ต้องมีไอเทม Heal) กด **Space bar** เพื่อยิงปืน และสามารถกด **1, 2** เพื่อสลับปืนได้ โดยปืนในเกมจะมี 2 ประเภทคือ Shotgun ปืนนี้จะมีกระสุนที่จำกัด และปืน Pistol ปืนนี้จะมีกระสุนไม่จำกัดแต่ความเสียหายต่อซอมบี้นั้นน้อยมากๆ ต้องยิงซอบบี้โดน 10 นัดจึงจะจัดการได้ โดยในตอนเริ่มเกมนั้นจะยังไม่มีซอมบี้บุกมา ซึ่งช่วงนี้ก็คือช่วงพักระหว่าง WAVE โดยในตอนเริ่มเกมนั้นคือ WAVE0 โดยในช่วงพักผู้เล่นสามารถซื้อของได้ โดยพ่อค้าจะปรากฎตัวออกมาให้เห็น เมื่อเราเดินเข้าไปชนกับพ่อค้าจะปรากฎปุ่มขึ้นมาโดยให้ใช้ เมาส์กด แล้วจะมีหน้าต่างขึ้นมา ให้เราสามารถอัพพลังชีวิตและความเร็วของผู้เล่นได้ในราคา 20 บาท โดยเงินจะได้จากการจัดการซอมบี้ และสามารถซื้อกระสุนกับยา ได้ในราคา 10 บาท โดยการที่เราจะเริ่ม WAVE นั้นต้องเดินไปชนกับ โน๊ตบุ๊คสีแดงตรงกลางแมพ ซึ่งจะปรากฎปุ่มขึ้นมาให้กดเริ่ม WAVE จากนั้นซอมบี้ก็จะแห่กันอออกมาจากรอบแมพมาหาผู้เล่น โดยซอมบี้เมื่อจัดการได้จะมีโอกาส **50%** ที่จะดรอป item เป็น กระสุนปืน และ ยา เมื่อจัดการกับซอมบี้จนหมดเวฟแล้วจะเข้าสู้ช่วงพัก และเตรียมเข้าสู่ WAVE ต่อไปที่ซอมบี้จะเก่งมากขึ้น!
## การทำงานของ Code
 ในไฟล์ main.py ในส่วนของคลาส app หลักนั้น ชื่อว่า **MyGameApp(App)** ที่ด้านในการใช้ **ScreenManager()** ในการจัดการหน้าจอในแอปโดยจะมีการเพิ่มหน้าจอเข้าไปดังนี้
 - หน้าจอ **main_menu** ที่จะใช้คลาส MainMenu()
 - หน้าจอ **game** ที่จะใช้คลาส GameScreen()
 - หน้าจอ **end_game** ที่จะใช้คลาส EndGame()

 โดยจะสามารถควบคุมการเปลี่ยนหน้าผ่านการใช้ app.root.current = '(Screen name)' ในไฟล์ .kv ได้
### โดย class ทั้งหมดใน code นี้ประกอบด้วย
 1. MainMenu(Screen)
 2. EndGame(Screen)
 3. GameScreen(Screen)
 4. UpgradePopup(Popup)
 5. WaveLabel(Widget)
 6. Obstacle(Image)
 7. Bullet(Widget)
 8. Enemy(Widget)
 9. Player(Widget)
 10. Heal_item(Widget)
 11. Ammo_item(Widget)
 12. MyGameApp(App) --> ได้อธิบายไปแล้ว

#### MainMenu(Screen)
 เป็นคลาสที่จัดการหน้าจอในส่วนของหน้าแรกของเกม โดยเมื่อเริ่มหน้าจอนี้นั้น **init** จะมีการใช้ Clock เพื่อผูกให้ตรวจสอบจำนวน 60 ครั้งใน 1 วินาทีกับเมธอด update ที่เป็นเมธอดสำหรับการตรวจเช็คค่าต่างๆตลอดเวลา (โดยจะใช้หลักการนี้ในหลายๆคลาสหลังจากนี้) และภายในคลาสนี้ประกอบด้วยเมธอดดังนี้
 - **on_enter()**  
    เป็นเมธอดที่มีมาอยู่แล้วกับคลาสแม่อย่าง Screen ที่จะทำคำสั่งดังนี้เมื่อเข้าสู่หน้าจอ โดยภายในเมธอดนี้จะทำการโหลด Music ด้วย **SoundLoader.load()** เพื่อทำการเปิดเพลงเมื่อเข้าเกม
- **update(dt)**  
    ภายในเมธอดนี้นั้นจะถูกตรวจเช็คตลอดเวลาเพราะมีการใช้ Clock โดยภายในนี้จะเช็คว่าเพลงเล่นอยู่มั้ยหากเล่นอยู่ให้ผูก volume ของเพลงกับ Slider ที่เป็นตัวปรับค่าแบบเส้นที่อยู่ในไฟล์ .kv เพื่อให้สามารถปรับระดับเสียงผ่าน Slider ได้
- **sound_test()**  
    เป็นเมธอดที่ผูกกับปุ่มใน .kv เมื่อทำการกดปุ่มจะเรียกใช้ฟังก์ชันนี้ฟังก์ชันนี้จะทำการเปิดเสียง SFX เพื่อให้สามารถเทสความดังของเอฟเฟคได้เมื่อปรับ Slider ในส่วน SFX
- **on_leave()**  
    เป็นเมธอดที่มีมาอยู่แล้วกับคลาสแม่อย่าง Screen ที่จะทำคำสั่งดังนี้เมื่อเข้าออกจากหน้าจอ โดยภายในนี้จะทำการสั่งปิด Music ที่เล่นในหน้าหลักกันเพลงซ้อน และทำการใช้ manager.get_screen('game') เพื่อเรียกใช้เมธอดของอีกคลาสหนึ่งเพื่อส่งค่าความดังของ Music และ SFX ที่ได้ปรับใน Slider ไปยังคลาส GameScreen(Screen)
#### EndGame(Screen)
 เป็นคลาสที่จัดการหน้าจอในส่วนของหน้าจบของเกมโดยมีการใช้ NumericProperty() กับค่า total_score และ wave เพื่อให้มันอัพเดทค่าไปยังส่วนที่เรียกใช้เมื่อมันเปลี่ยนแปลง โดยภานในคลาสมีเมธอด
 - **update_score(score)**  
    เมธอดนี้จะถูกเรียกใช้จากอีกคลาสเพื่อเป็นตัวส่งค่าจากอีกคลาสมาคลาสนี้และนำค่าที่ได้มาเปลี่ยนใน total_score เพื่อนำไปแสดงผลเป็นข้อความโชว์คะแนน
- **update_wave(wave)**  
    เมธอดนี้มีหลักการเดียกับเมธอด update_score เพื่อนำมาเก็บไว้ใน wave เพื่อนำไปแสดงผลข้อความในไฟล์
#### GameScreen(Screen)
 เป็นคลาสที่จัดการหน้าจอในส่วนของหน้าเกมหลักโดยมีการใช้ NumericProperty() กับค่า enemy_counts และ wave_game เพื่อให้ส่วนอื่นที่นำไปใช้อัพเดทค่าตามเมื่อมีการเปลี่ยนแปลง และภายใน __init__            มีการกำหนดค่าคุณสมบัติต่างๆที่นำไปใช้ในคลาสนี้ให้ปรับได้ง่ายๆโดยสามารถเข้าใจได้โดยชื่อ และมีการใช้ Clock เพื่อใช้ตรวจเมธอด update ตลอด โดยภายในคลาสนี้มีเมธอด
 - **create_enemy(dt)**  
    เป็นเมธอดสร้าง enemy ที่จะมีการเรียกใช้ผ่าน Clock โดยภายในนี้จะมีการสุ่มที่เกิดของ enemy แต่ละตัวและทำการวนสร้าง enemy ผ่านค่าจำนวนของ enemy (self.enemies.now)โดยจะมีการเก็บ **enemy เป็น dict ใน self.enemies ไว้ด้วยเพื่อให้สามารถนำไปตรวจเช็ค enemy แต่ละตัวๆได้ง่ายในภายหลัง** และเมื่อทำการวนลูปสร้างเสร็จจะเรียกใช้เมธอด **next_game_value()**
 - **create_obstacle**  
    เป็นเมธอดที่มีพารามิเตอร์ positions และ images เป็นลักษณะ list โดยค่า positions คือ list ของตำแหน่งของ obstacle แต่ละอัน และ images คือ list ของที่อยู่ภาพ โดยทั้งสองมี index ที่สัมพันธ์กัน โดยจะมีการสร้าง object ของคลาส Obstacle() ขึ้นเพื่อเป็นลักษณะของ obstacle ของแต่ละอัน โดยจะมีใช้ค่าพารามิเตอร์ทั้งสองกำหนดภาพและตำแหน่งของ obstacle แต่ละอันจากนั้นนำมา add_widget ในหน้าจอ และทำการเก็บ object ไว้ใน list (หลักการเดียวกับ enemy )
 - **update(dt)**  
    เป็นเมธอดที่ทำตลอดเวลาโดยภายในนี้จะสั่งให้ enemy แต่ละตัวที่เก็บไว้ใน self.enemies เรียกใช้เมธอดของตัวเองคือเดินตามผู้เล่น และมีการเรียกใช้เมธอดของตัวเอง **end_wave()**
 - **on_enter()**  
    ทำเมื่อเข้าสู่หน้านี้ เปิดให้ผู้เล่น(id)ให้สามารถใช้คีย์บอร์ดได้ โดยผู้เล่นเป็น object ของคลาส Player และกำหนดค่าตำแหน่งในของ obstacles และที่อยู่ภาพของ obstacles เพื่อส่งไปให้เมธอด **creat_obstacle()** ทำการสร้าง obstacle
- **on_leave()**  
    ทำเมื่ออกจากหน้านี้ ปิดคีย์บอร์ดผู้เล่น และวนค่า self.enemies สั่งทุกตัวให้ปิดการทำงาน และทำการกดหนดค่าต่างๆที่เปลี่ยนไประหว่างการเล่นให้เป็นค่าเริ่มต้น (reset) และทำการปิดเพลงพื้นหลัง
- **minus_player_hp(enemy_id)**  
    เมธอดนี้จะถูกเรียกใช้โดย widget ลูกโดยจะทำการลดเลือดของ player ตามดาเมจของ enemy และทำการปิด enemy id นั้น จากนั้นใช้ Clock เพื่อให้ทำครั้งเดียวหลักจากผ่านไป 4 วิ เพื่อทำให้เกิดการ cooldown (ไม่ตีซ้ำรัวๆ) โดยเมื่อครบจะเรียกใช้เมธอด **re_enable_enemy()** และส่งค่า enemy_id เข้าไป
- **re_eneble_enemy(enemy_id)**  
    ทำการเช็คว่ามี enemy id นี้อยู่ใน self.enemies มั้ยและทำการเปิดการทำงานหากมี
- **minus_enemy_hp(enemy_id, damage)**  
    ทำการเช็คว่า enemy id นี้มีเลือดไม่เท่ากับ 0 ใช่มั้ยและทำการลดเลือด enemy id นั้นจากค่าอากิวเมนต์ damage และทำการเช็คต่อว่า enemy id นั้น เลือดเหลือ 0 มั้ยหากใช่ ปิด enemy id นั้นและลบออกจาก widget ของหน้า game และลบค่า object ออกจาก self.enemies
- **end_wave()**  
    เมธอดนี้จะถูกเช็คตลอดเวลาผ่าน update เพื่อให้เมื่อจบ WAVE จะโชว์ store และ ปุ่มต่างๆ เมธอดนี้จะตรวจเช็คว่า ผู้เล่นได้เดินชนกับ id nw_ob และ enemy_left เท่ากับ 0 หรือป่าวถ้าใช่ให้ขึ้นปุ่มถ้าไม่ไม่ต้องขึ้น และทำนองเดียวกันเช็คกับตัว Store ว่าชนหรือไม่แล้วทำการโชว์ปุ่มไม่โชว์ปุ่ม
- **next_wave()**  
    เป็นเมธอดที่เมื่อมีการเรียกใช้จากปุ่ม (ใน .kv) จะทำการอัพเดทค่า wave_game และค่า enemy_counts (enemy ที่เหลือใน wave)และใช้ Clock เพื่อสร้างดีเลย์รอ 3 วิจากนั้นเรียกใช้เมธอด **create_enemy()** และเรียกใช้ Sound ด้วย SoundLoader.load() และทำการสร้างข้อความโชว์ WAVE ที่หน้าจอโดยใช้วิธีสร้าง object ข้อความที่เป็น object ของคลาส WaveLabel และทำการ add_widget ลงหน้าเกม จากนั้นเรียกใช้เมธอด show_message ของ object ข้อความ WAVE
- **show_upgrade_popup()**  
    เป็นเมธอดที่ถูกเรียกใช้เมื่อกดปุ่ม (ใน .kv) โดยจะทำการสร้าง popup ขึ้นเพื่อเป็น object ของคลาส UpgradePopup() และเรียกใช้เมธอด open() เพื่อโชว์ popup ร้านค้าขึ้นมา และโหลด Sound ผ่าน SoundLoader.load()
- **next_game_value()**  
    เมื่อเรียกใช้จำทำการปรับค่าของเกมใน WAVE ถัดไปให้มีความยากขึ้น
- **end_game()**  
    เมื่อเรียกใช้จะทำการส้่งค่าไปยังอีกจอ (end_game) โดยใช้ manager.get_screen() จากนั้นส่งค่า player score, wave_game ไปเพื่อไปโชว์ในหน้าสุดท้าย และทำการปรับจอไปยังหน้า end_game โดยใช้ self.manager.current
- **update_volume(bg_volume, sfx_volume)**  
    ปรับค่าเสียงที่ได้รับมาจากอีกคลาส และสั่งให้เริ่มเล่น Music พื้นหลัง
#### UpgradePopup(Popup)
 เป็นคลาส pop up ร้านค้า ใน __init__ มีการกำหนดค่าราคาของไอเทมและการอัพเกรด และผูกค่าเงินที่แสดงในร้าน เมธอด
 - **update_coin(instance, value)**  
    เป็นเมธอดที่ผูกไว้กับค่าเงินของ parent.ids.player
- **upgrade_speed()**  
    จะถูกเรียกใช้จากปุ่มใน (.kv) เพื่อทำการเช็คเงินลดเงินและเพิ่มค่าอัพเดทให้ speed หากเงินพอและเรียกใช้เมธอด **buying_sound()**
- **upgrade_hp()** , **buy_bullet()**, **buy_heal()** มีลักษณะเดียวกันกับ **upgrade_speed()**  
- **buying_sound()**  
    เล่นเสียงซื้อของผ่าน SoundLoader.load()
#### WaveLabel()
 เป็นคลาสที่จะสร้าง Label Wave ตามด้วยเลขขึ้นมาเพื่อโชว์ในหน้าจอ game 
- **on_parent(instance, parent)**  
    ปรับ position บน widget parent
- **show_mesage() and remove_widget_from_parent(*args)** 
    แสดงAnimation ค่อยๆเพิ่มความเข้มจางของตัวหนังสือและค่อยๆลดลง โดยใช้ Animation จากนั้นผูกเข้ากับเมธอด **remove_widget_from_parent()** เพื่อให้เมื่อจบ Animation ทำการลบ widget นี้ทิ้งจาก parent
#### Obstacle()
 เป็นคลาสว่างที่มีไว้ระบุ Obstacle
#### Bullet()
 เป็นคลาสของกระสุนแต่ละนัดที่จะถูกสร้างขึ้นโดยมีค่าคุณสมบัติใน __init__ คือ pos, rotation, velocity, damage และมีการใช้ Clock เพื่อให้ทำเมธอด move_bullet ตลอดเวลา
- **move_bullet(dt)**  
    เป็นเมธอดที่ทำงานตลอดเวลาคือจะทำการคำนวณค่า x, y และทิศทางผ่านค่า rotation ของกระสุน ทำให้กระสุนสามารถเคลื่อนที่ไปได้ในหน้าจอ และมีการเช็คการชนของวัตถุโดยจะเช็คว่าได้ชนกับ enemy ตัวไหนมั้ยโดยใช้เมธอด **collide_with_enemy** หากชนเล่น Sound จากนั้นเรียกใช้ minus_enemy_hp(enemy_id, self.damage) ของ parent เพื่อลดเลือด enemy จากนั้นเรียกเมธอด **remove_bullet()** และ break หากไม่ชนกับ enemy ตัวไหนเลยจะไปเช็คอีกเงื่อนไขคือชนกับกำแพงหรือป่าวถ้าชน ก็เรียกเมธอด **remove_bullet()**
- **collide_with_enemy(enemy_pos, enemy_size)**  
    เมธอดนี้เมื่อเรียกใช้จะคำนวณว่ากระสุนได้ชนกับ enemy ตัวนี้หรือป่าว โดยจะ return เป็น True False
- **remove_bullet()**
    เมธอดนี้เมื่อเรียกใช้จะทำการให้ parent ลบ widget ตัวเองออก
#### Enemy(Widget)
 เป็นคลาสของ enemy แต่ละตัวเมื่อมีการสร้าง โดยมีคุณสมบัติค่า speed, id, enable?, get_player?, และค่าของมุมที่ไว้ใช้ในการคำนวณอัลกอรึทึมให้ enemy มัน detect player และ หลบเลี่ยง obstacles | มีการใช้ Clock เช็คตรวจเวลากับเมธอด **debug_values()**
- **debug_values(dt)**  
    เช็คว่าเลือดมีน้อยกว่า 0 มั้ยถ้าใช่ให้เซ็ตเป็น 0 (กันเลือดติดลบ)
- **enable_enemy()**  
    เซ็ตค่า self.enable = True
- **disable_enemy()**  
    เซ็ตค่า self.enable = False และเช็คต่อว่า enemy เลือดเหลือ 0 หรือยัง ถ้าใช่ให้เพิ่ม score ไปที่ player ลดค่า enemy_counts ของเกม เพิ่มเงินให้ player จากนั้นทำการสุ่มโอกาส 50% ว่าจะมี item ดรอปมั้ย ถ้าได้เรียก **spawn_item(self.pos, self.enemy_id)** และย้าย enemy ให้ออกจากหน้าจอก่อน
- **collide_with_obstacle()**  
    เป็นเมธอดที่จะเช็คว่าตอนนี้กระสุนนัดนี้ได้ชนกับ obstacle ตัวไหนหรือป่าวถ้าชน return True ไม่ False
- **find_clear_path(angle)**  
    เป็นเมธอดที่ใช้เพื่อคำนวณเพื่อหาเส้นทางใหม่โดยการหันหน้าเพิ่ม 15 องศา เมธอดนี้ใช้กับ follow_player() เพื่อหลบ obstacles
- **follow_player(player_pos, player_size, dt)**  
    เป็นเมธอดที่ถูกเรียกใช้ตลอดเวลาผ่าน Clock ใน parent อย่างหน้า game (GameScreen()) เป็นเมธอดการคำนวณเดินหลักของ enemy ที่จะตาม player ไปตรวจเช็คชนกำแพงหรือป่าวชน obstacles มั้ยโดยจะใช้ค่า x, y และ rotation เป็นหลัก