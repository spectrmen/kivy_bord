# Программа, чтобы показать, как использовать textinput (виджет UX) в kivy


# импорт кивый модуль

import kivy


# Базовый класс вашего приложения наследуется от класса приложения.
# app: всегда ссылается на экземпляр вашего приложения

from kivy.app import App


# это ограничивает kivy версию т.е.
# ниже этой версии вы не можете
# использовать приложение или программное обеспечение

kivy.require('1.9.0')


# Виджет «Метка» предназначен для визуализации текста.

from kivy.uix.label import Label


# модуль состоит из floatlayout
# сначала работать с FloatLayout
# вы должны импортировать его

from kivy.uix.floatlayout import FloatLayout


# Scatter используется для построения интерактивных
# виджеты, которые можно перевести,
# повернуто и масштабировано с двумя или более
# пальцы в мультитач-системе.

from kivy.uix.scatter import Scatter


# Виджет TextInput предоставляет
# поле для редактирования простого текста

from kivy.uix.textinput import TextInput


# BoxLayout упорядочивает виджеты либо
# по вертикали, что
# один поверх другого или в
# горизонтальная мода, которая одна за другой.

from kivy.uix.boxlayout import BoxLayout


# Создать класс приложения

class TutorialApp(App):



    def build(self):



        b = BoxLayout(orientation ='vertical')



        # Добавление текстового ввода

        t = TextInput(font_size = 50,

                      size_hint_y = None,

                      height = 100)



        f = FloatLayout()



        # По этому вы можете двигаться

        # Текст на экране куда угодно

        s = Scatter()



        l = Label(text ="Hello !",

                  font_size = 50)



        f.add_widget(s)

        s.add_widget(l)



        b.add_widget(t)

        b.add_widget(f)



        # Привязка к этикетке

        t.bind(text = l.setter('text'))





        return b


# Запустите приложение

if __name__ == "__main__":

    TutorialApp().run()
