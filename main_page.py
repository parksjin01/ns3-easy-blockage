from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class TitleSection(Widget):
    pass

class SelectSection(Widget):
    pass

class SceneSection(Widget):
    pass

class CodeSection(Widget):
    pass

class MainBoard(Widget):
    pass

class MainBoardApp(App):
    def build(self):
        return MainBoard()


if __name__ == '__main__':
    MainBoardApp().run()