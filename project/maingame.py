import kivy
kivy.require('2.3.1')

from kivy.app import App
from kivy.uix.label import Label

class MyGameApp(App):
    def build(self):
        return Label(text='Hello World')
    
if __name__ == '__main__':
    MyGameApp().run()
