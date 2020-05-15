from kivy.app import App
from itertools import zip_longest
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import (Color, Rectangle, RoundedRectangle)
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from fuzzywuzzy import process
import csv

class BordObject(Widget):
    class NumberHome(TextInput):
        def __init__(self, *args):
            super().__init__(*args)
            self.LIMIT = 5
            self.size_hint=(None, None)
            self.background_color=(0,0,255,1)
            self. multiline=False
            self.font_size='90dp'
            self.foreground_color=(255,255,255,1)
        def insert_text(self, text, from_undo=False):
            if len(self.text)>self.LIMIT:
                return False
            return super().insert_text(text, from_undo=from_undo)
        def update_font(self):
            if len(self.text) <= 2:
                self.font_size = '100dp'
            elif len(self.text) == 3:
                self.font_size = '70dp'
            elif len(self.text) == 4:
                self.font_size = '60dp'
            elif len(self.text) == 5:
                self.font_size = '50dp'
            elif len(self.text) == 6:
                self.font_size = '40dp'
        def update_padding(self, *args):
            self.padding_y = self.height / 2 - (self.line_height / 2)

    def __init__(self, **kwards):
        super().__init__(**kwards)
        #загружаем улицы в объект
        ''' может надо переделать?'''
        with open('streats.csv', newline='\n') as f:
            self.streets = []
            for row in csv.reader(f):
                    self.streets.append(tuple(row))
        self.only_streers = list(map(lambda x: x[0], self.streets))
        self.only_prefix = list(map(lambda x: x[1], self.streets))
        #Создаем лебл
        self.TOP_SHIFT = 20
        self.SHIFT_HEADER = 70
        self.rect = RoundedRectangle()
        self.home_number =  self.number_home()
        self.lbl = Label(
                    text= self.streets[0][0],
                    font_size='100dp',
                    size_hint=(None, None),
                    color=(255,255,255,1),
                    padding=[50, 20]
                    )
        self.header = Label(
                    text= self.streets[0][1],
                    font_size='50dp',
                    size_hint=(None, None),
                    color=(255,255,255,1))
        self.render()
        self.lbl.bind(text=self.update_all) #связка с полем lbl
        self.home_number.bind(text=self.update_num)

    def render(self):
        self.canvas.clear()
        print( 'i working in render %s' % self.lbl.size )
        '''создание номера'''
        self.canvas.before.add(Color(255, 255, 255, 1))
        self.canvas.before.add(self.rect)
        self.canvas.ask_update()
        self.add_widget(self.lbl)
        self.add_widget(self.header)
        self.add_widget(self.home_number)
    @classmethod
    def number_home(Class):
        return Class.NumberHome()
    '''динамика'''
    def update_all(self, *args):
        self.update_lbl()
        self.update_rect()
        self.update_num()
        self.update_header()

    def update_lbl(self, *args):
        self.lbl.text = process.extractOne(self.lbl.text, self.only_streers)[0]
        self.lbl._label.refresh()
        self.lbl.size = self.lbl._label.texture.size
        self.lbl.pos = (self.center_x-self.lbl.size[0]/2,
                         self.center_y-self.lbl.size[1]/2)
    def update_header(self, *args):
        self.header.text = self.only_prefix[self.only_streers.
                                            index(self.lbl.text)]
        self.header._label.refresh()
        self.header.size = self.lbl._label.texture.size
        self.header.pos = (self.center_x-self.lbl.size[0]/2,
                         self.center_y-self.lbl.size[1]/2 + self.SHIFT_HEADER)

    def update_rect(self, *args):
        self.rect.size = self.lbl.size
        self.rect.pos = [self.lbl.pos[0], self.lbl.pos[1]+self.TOP_SHIFT]

    def update_num(self, *args):
        self.home_number.size = (self.lbl.size[1], self.lbl.size[1])
        self.home_number.pos = (self.lbl.pos[0]+self.lbl.size[0],
                                 self.lbl.pos[1]+self.TOP_SHIFT)
        self.home_number.update_font()
        self.home_number.update_padding()

    def clear_canvas(self, instance):
        self.canvas.clear()

    def save(self, instance):
        self.export_to_png('image.png')

class bordApp(App):
    def build(self):

        Window.clearcolor = (100, 0, 0, 1)
        parent = BoxLayout(orientation='vertical')
        self.painter = BordObject(size=(Window.size[0], Window.size[1]))
        print(dir(self.painter))
        self.textinput = TextInput(text='введите название улицы',font_size = 50,
                      size_hint_y=None,
                      height=100,
                      multiline=False)
        parent.add_widget(self.textinput)
        parent.add_widget(self.painter)
        blh = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))

        blh.add_widget(Button(text = 'Save', on_press=self.painter.save,
                                 size=(100,50)))
        blh.add_widget(Button(text='Clear',
                                  on_press=self.painter.clear_canvas,
                                 size=(100,50), pos=(200,0)))
        parent.add_widget(blh)
        '''связывание поляввода и метки'''
        self.textinput.bind(text = self.painter.lbl.setter('text'))
        return parent

if __name__ == "__main__":
    bordApp().run()
