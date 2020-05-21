from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.graphics import (Color,Line, Rectangle, RoundedRectangle)
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from FileDialog import SaveDialog
from fuzzywuzzy import process
from transliterate import translit
import csv
from fonts import import_fonts
import os
#добавление новых шрифтов
import_fonts()

from kivy.uix.popup import Popup

class BordObject(Widget):
    class NumberHome(TextInput):
        def __init__(self,*args):
            super().__init__(*args)
            self.LIMIT = 4
            self.PADDING = 20
            self.size_hint = (None, None)
            self.background_color = (0,0,255,1)
            self. multiline = False
            self.font_size = '90dp'
            self.foreground_color = (255,255,255,1)

        def insert_text(self, text, from_undo=False):
            if len(self.text)>self.LIMIT:
                return False
            return super().insert_text(text, from_undo=from_undo)

        def on_text(self,instance, value):
            self.update_font()
            self.update_padding()

        def update_font(self):
            if len(self.text) <= 2:
                self.font_size = '90dp'
            elif len(self.text) == 3:
                self.font_size = '70dp'
            elif len(self.text) == 4:
                self.font_size = '60dp'
            elif len(self.text) == 5:
                self.font_size = '50dp'
            elif len(self.text) == 6:
                self.font_size = '40dp'

        def update_padding(self, *args):
            self.text_width = self._get_text_width(
            self.text,
            self.tab_width,
            self._label_cached)
            self.padding_x = (self.width - self.text_width) / 2
            self.padding_y = self.height / 2 - self.line_height / 2

    def __init__(self, **kwards):
        super().__init__(**kwards)
        #загружаем улицы в объект
        ''' может надо переделать?'''
        with open('streats.csv', newline='\n') as f:
            self.streets = []
            for row in csv.reader(f):
                    self.streets.append(tuple(row))
        self.only_streets = list(map(lambda x: x[0], self.streets))
        self.only_prefix = list(map(lambda x: x[1], self.streets))
        #Создаем лебл
        self.SHIFT_RECT = -10
        self.WIDTH_RECT = 150
        self.SHIFT_HEADER = 50
        self.SHIFT_LATIN = -50
        self.FONT = 70
        self.SHIFT_ARROW_RIGHT = -5
        self.SHIFT_X = 70
        self.SHIFT_Y = 30
        self.SHIFT_ARROW_LEFT = 95
        self.rect = Rectangle()
        self.border = Line(width=1,
                           joint="round",
                           close=True)
        self.lbl = Label(
                    text=self.only_streets[0],
                    font_size=self.FONT,
                    size_hint=(None, None),
                    color=(255,255,255,1),
                    padding=[50, 20],
                    font_name="Alice"
                    )
        self.header = Label(
                    text=self.streets[0][1],
                    font_size=self.FONT - 30,
                    size_hint=(None, None),
                    color=(255,255,255,1),
                    font_name="Charis")
        self.latin_title = Label(
                    font_size=self.FONT - 40,
                    size_hint=(None, None),
                    color=(255,255,255,1),
                    font_name="Alegreya",
                    italic=True
                    )
        self.home_number =  self.number_home()
        self.button_right = Button(text="",
                                  font_size=20,
                                  color=(0,0,0,1),
                                  background_color=(255,255,255,1),
                                  size=(30,30),
                                  font_name="icons",
                                  on_press=self.upper_number)
        self.button_left = Button(text="",
                                  font_size=20,
                                  color=(0,0,0,1),
                                  background_color=(255,255,255,1),
                                  size=(30,30),
                                  size_hint=(None, None),
                                  font_name="icons",
                                  on_press=self.lower_number)
        self.label_right = Label(text='2',
                           font_size='25dp',
                           color=(255,255,255,1))
        self.label_left = Label(text='0',
                           font_size='25dp',
                           color=(255,255,255,1))
        self.render()
        self.lbl.bind(text=self.update_all) #связка с полем lbl
        #изменение размера рамки
        self.bind(size=self.update_all)

    def render(self):
        self.canvas.clear()
        '''создание номера'''
        self.canvas.before.add(Color(255, 255, 255, 1))
        self.canvas.before.add(self.rect)
        self.canvas.before.add(Color(0, 0, 0, 3))
        self.canvas.before.add(self.border)
        self.canvas.ask_update()
        self.add_widget(self.lbl)
        self.add_widget(self.header)
        self.add_widget(self.home_number)
        self.add_widget(self.latin_title)
        self.add_widget(self.label_right)
        self.add_widget(self.button_right)
        self.add_widget(self.label_left)
        self.add_widget(self.button_left)
    @classmethod
    def number_home(Class):
        return Class.NumberHome()
    '''динамика'''
    def update_all(self, *args):
        self.update_lbl()
        self.update_rect()
        self.update_header()
        self.update_num()
        self.update_latin()
        self.update_arrow()



    def update_pos(self, obj, shift=0):
        obj.size = obj._label.texture.size
        obj.pos = (self.center_x-obj.size[0]/2,
                         self.center_y-obj.size[1]/2+shift)

    def update_lbl(self, *args):
        self.lbl.text = process.extractOne(self.lbl.text, self.only_streets)[0]
        self.lbl._label.refresh()
        self.update_pos(self.lbl)

    def update_latin(self, *args):
        self.latin_title.text = translit(self.lbl.text, reversed=True) + \
                                        ' street'
        self.latin_title._label.refresh()
        self.update_pos(self.latin_title, shift=self.SHIFT_LATIN)

    def update_header(self, *args):
        self.header.text = self.only_prefix[self.only_streets.
                                            index(self.lbl.text)]
        self.header._label.refresh()
        self.update_pos(self.header, self.SHIFT_HEADER)

    def update_rect(self, *args):
        self.rect.size = [self.lbl.size[0]+self.home_number.size[0],
                          self.WIDTH_RECT]
        self.rect.pos = [self.lbl.pos[0], self.lbl.pos[1]+self.SHIFT_RECT]
        self.border.rectangle = (self.rect.pos[0], self.rect.pos[1], self.rect.size[0], self.rect.size[1])

    def update_num(self, *args):
        self.home_number.size = (self.rect.size[1]-self.home_number.PADDING,
                                  self.rect.size[1]-self.home_number.PADDING)
        self.home_number.pos = (self.lbl.pos[0]+self.lbl.size[0]-self.home_number.PADDING/2,
                                 self.lbl.pos[1]+self.SHIFT_RECT+self.home_number.PADDING/2)
        self.home_number.update_font()
        self.home_number.update_padding()

    def update_arrow(self, *args):
       self.label_right.pos = (self.center_x+self.rect.size[0]/2-\
                               self.home_number.size[0]+self.SHIFT_ARROW_RIGHT-\
                                self.SHIFT_X, self.latin_title.pos[1] - self.SHIFT_Y)
       self.button_right.pos = (self.center_x+self.rect.size[0]/2-\
                                self.home_number.size[0]+self.SHIFT_ARROW_RIGHT,
                                self.latin_title.pos[1] + 10)
       self.label_left.pos = (self.center_x-self.rect.size[0]/2 + 100,
                                self.latin_title.pos[1] - self.SHIFT_Y)
       self.button_left.pos = (self.center_x - self.rect.size[0]/2+self.SHIFT_ARROW_LEFT,
                                self.latin_title.pos[1] + 10)

    def clear_canvas(self, instance):
        self.canvas.clear()

    def upper_number(self, *args):
        self.label_right.text = str(int(self.label_right.text) + 1)
        self.label_left.text = str(int(self.label_left.text) + 1)

    def lower_number(self, *args):
        self.label_right.text = str(int(self.label_right.text) - 1)
        self.label_left.text = str(int(self.label_left.text) - 1)

class bordApp(App):
    def save(self, path, filename):
        self.painter.export_to_png(os.path.join(path, filename))
        self._popup.dismiss()

    def show_save(self, instance):
        content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
        self._popup = Popup(title="Save file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def dismiss_popup(self):
        self._popup.dismiss()

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

        blh.add_widget(Button(text='Обновить',
                              on_release=self.painter.update_all,
                                 size=(100,50)))
        blh.add_widget(Button(text='Сохранить',
                              on_release=self.show_save,
                                 size=(100,50), pos=(200,0)))
        parent.add_widget(blh)
        '''связывание поляввода и метки'''
        self.textinput.bind(text = self.painter.lbl.setter('text'))
        return parent

if __name__ == "__main__":

    bordApp().run()
