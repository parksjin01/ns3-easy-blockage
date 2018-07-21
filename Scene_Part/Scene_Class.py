from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import json

import main_page

class Touch_Handle():
    def __init__(self, root):
        self.root = root

    def on_touch_down(self, touch):

        try:
            with open(main_page.fild_directory + main_page.file_name, 'r') as f:
                obstacle_list = json.load(f)
        except:
            obstacle_list = {"obstacle_list":[]}

        x, y = touch.pos
        label = Label(text=main_page.current_obstacle, center_x=touch.pos[0], center_y=touch.pos[1], color=(0, 0, 0, 1))
        if self.root.pos[0] + label.width/2 <= x and x <= self.root.pos[0] + self.root.size[0] - label.width/2:
            if self.root.pos[1] + label.height/2 <= y and y <= self.root.pos[1] + self.root.size[1] - label.height/2:
                self.root.add_widget(label, index=1)

                obstacle = {}
                obstacle['title'] = main_page.current_obstacle
                obstacle['position'] = touch.pos
                obstacle['size'] = label.size
                obstacle_list['obstacle_list'].append(obstacle)

                with open(main_page.fild_directory + main_page.file_name, 'w') as f:
                    json.dump(obstacle_list, f)

class Scene(Widget):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
    def on_touch_down(self, touch):
        touch_handle = Touch_Handle(self)
        touch_handle.on_touch_down(touch)