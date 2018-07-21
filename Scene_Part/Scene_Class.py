from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import json

import main_page

class Touch_Handle():
    def __init__(self, root):
        self.root = root
        try:
            with open(main_page.file_dir + main_page.file_name, 'r') as f:
                self.obstacle_list = json.load(f)
                for obstacle in self.obstacle_list['obstacle_list']:
                    image = Image(source=main_page.icon_dir + obstacle['image'],
                                  center_x=obstacle['position'][0], center_y=obstacle['position'][1])
                    self.root.add_widget(image, index=1)
        except Exception, e:
            self.obstacle_list = {"obstacle_list":[]}

    def on_touch_down(self, touch):

        if main_page.current_obstacle == {}:
            return

        x, y = touch.pos
        image = Image(source = main_page.icon_dir + main_page.current_obstacle['Image'], center_x=touch.pos[0], center_y=touch.pos[1])
        if self.root.pos[0] + image.width/2 <= x and x <= self.root.pos[0] + self.root.size[0] - image.width/2:
            if self.root.pos[1] + image.height/2 <= y and y <= self.root.pos[1] + self.root.size[1] - image.height/2:
                self.root.add_widget(image, index=1)

                obstacle = {}
                obstacle['title'] = main_page.current_obstacle['Name']
                obstacle['position'] = touch.pos
                obstacle['size'] = main_page.current_obstacle['Initial_Size']
                obstacle['image'] = main_page.current_obstacle['Image']
                self.obstacle_list['obstacle_list'].append(obstacle)

                with open(main_page.file_dir + main_page.file_name, 'w') as f:
                    json.dump(self.obstacle_list, f)

    def on_touch_move(self, touch):
        print touch

class Scene(Widget):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
        self.touch_handle = Touch_Handle(self)
    def on_touch_down(self, touch):
        self.touch_handle.on_touch_down(touch)

    def on_touch_move(self, touch):
        self.touch_handle.on_touch_move(touch)