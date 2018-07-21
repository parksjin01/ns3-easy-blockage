from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView
from kivy.adapters.simplelistadapter import SimpleListAdapter
from kivy.uix.label import Label
from kivy.properties import NumericProperty, ReferenceListProperty, BooleanProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

from Select_Part.Select_Class import *
from Scene_Part.Scene_Class import *

current_obstacle = "Clicked"
fild_directory = "Obstacle_Locations/"
file_name = "test.json"

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