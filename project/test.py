from kivy.app import App
from kivy.clock import Clock
from kivy.uix.label import Label

class MyApp(App):
    def build(self):
        return Label(text="Hello, Kivy!")

    def on_start(self):
        # เรียกใช้ฟังก์ชันหลังจาก 1 วินาที
        Clock.schedule_once(self.start_function, 1)

    def start_function(self, dt):
        print("App started after 1 second")

if __name__ == '__main__':
    MyApp().run()