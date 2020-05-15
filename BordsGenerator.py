from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import (Color, Rectangle)
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from fuzzywuzzy import process
import csv

class BordObject(Widget):
    def __init__(self, **kwards):
        super().__init__(**kwards)
        #загружаем улицы в объект
        ''' может надо переделать?'''
        with open('streats.csv', newline='\n') as f:
            self.streets = []
            for row in csv.reader(f):
                    self.streets.append(tuple(row))
        self.only_streers = list(map(lambda x: x[0], self.streets))
        #Создаем лебл
        self.lbl = Label(
                    text= self.streets[0][0],
                    font_size='100dp',
                    size_hint=(None, None),
                    color=(255,255,255,1))
        self.render()
        self.lbl.bind(text=self.update_all) #связка с полем lbl
        #Clock.schedule_interval(self.callevery, 1)

    def get_street(self,text:str):
        street = process.extractOne(text, self.only_streers)
        return str(street[0])

    def render(self):
        self.canvas.clear()
        print( 'i working in render %s' % self.lbl.size )
        self.rect = Rectangle()
        '''создание номера'''
        self.lbl.canvas.before.add(Color(255, 255, 255, 1))
        self.lbl.canvas.before.add(self.rect)
        self.lbl.canvas.ask_update()
        self.create_num()
        self.add_widget(self.lbl)

    def create_num(self):
        self.border_num = Rectangle()
        self.home_number =  TextInput(size_hint=(None, None),
                                          background_color=(0,0,255,1),
                                          multiline=False,
                                          font_size='90dp',
                                          foreground_color=(255,255,255,1))
        #self.home_number.canvas.before.add(Color(255,255,255,1))
        #self.home_number.canvas.before.add(self.border_num)
        #self.home_number.canvas.ask_update()
        self.add_widget(self.home_number)
    '''динамика'''
    def update_all(self, *args):
        self.update_lbl()
        self.update_rect()
        self.update_num()

    def update_lbl(self, *args):
        self.lbl.text = self.get_street(self.lbl.text)
        self.lbl._label.refresh()
        self.lbl.size = self.lbl._label.texture.size
        self.lbl.pos = (self.center_x-self.lbl.size[0]/2,
                         self.center_y-self.lbl.size[1]/2)

    def update_rect(self, *args):
        self.rect.size = self.lbl.size
        self.rect.pos = self.lbl.pos
        print( 'i working %s' % self.lbl.size )

    def update_num(self, *args):
        self.home_number.size = (self.lbl.size[1], self.lbl.size[1])
        self.home_number.pos = (self.lbl.pos[0]+self.lbl.size[0],
                                 self.lbl.pos[1])
        self.border_num.size = (self.home_number.size[0]+2,
                                self.home_number.size[1]+2)
        self.border_num.pos = self.home_number.pos
    def clear_canvas(self, instance):
        self.canvas.clear()

    def save(self, instance):
        self.export_to_png('image.png')

class bordApp(App):
    def build(self):
        #Window.clearcolor = (100, 0, 0, 1)
        parent = BoxLayout(orientation='vertical')
        self.painter = BordObject(size=(Window.size[0], Window.size[1]))
        self.textinput = TextInput(text='введите название улицы',font_size = 50,
                      size_hint_y=None,
                      height=100,
                      multiline=False)
        parent.add_widget(self.textinput)
        parent.add_widget(self.painter)
        blh = BoxLayout(orientation='horizontal', size_hint=(1, 0.3))

        blh.add_widget(Button(text = 'Save', on_press=self.painter.save,
                                 size=(100,50)))
        '''blh.add_widget(Button(text = 'draw',
                                  on_press=self.painter.render,
                                 size=(100,50), pos=(100,0)))'''
        blh.add_widget(Button(text='Clear',
                                  on_press=self.painter.clear_canvas,
                                 size=(100,50), pos=(200,0)))
        parent.add_widget(blh)
        '''связывание поляввода и метки'''
        self.textinput.bind(text = self.painter.lbl.setter('text'))
        return parent

if __name__ == "__main__":
    bordApp().run()
