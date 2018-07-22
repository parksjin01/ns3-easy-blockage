from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

import json
import math

import main_page

def distance(point1, point2):
    dist = 0
    if len(point1) == len(point2):
        for idx in range(len(point1)):
            dist += (point1[idx] - point2[idx])**2
    return math.sqrt(dist)

def size(obstacle):
    try:
        return math.sqrt((obstacle['Initial_Size'][0]/2) ** 2 + (obstacle['Initial_Size'][1]/2) ** 2)
    except:
        return math.sqrt((obstacle['size'][0] / 2) ** 2 + (obstacle['size'][1] / 2) ** 2)

def collision_detect(obstacle_list, current_obstacle, pos):
    if obstacle_list == {}:
        return True, {}
    current_obstacle_size = size(current_obstacle)
    for obstacle in obstacle_list['obstacle_list']:
        obstacle_size = size(obstacle)
        if current_obstacle_size + obstacle_size > distance(obstacle['position'], pos):
            print obstacle['title'], current_obstacle_size, obstacle_size, distance(obstacle['position'], pos), obstacle['position'], pos
            return False, obstacle
    return True, {}


class Touch_Handle():
    def __init__(self, root):
        self.root = root
        try:
            with open(main_page.file_dir + main_page.file_name, 'r') as f:
                self.obstacle_list = json.load(f)
                for obstacle in self.obstacle_list['obstacle_list']:
                    image = Image(source=main_page.icon_dir + obstacle['image'], size=obstacle['size'][:2])
                    image.center_x = obstacle['position'][0]
                    image.center_y = obstacle['position'][1]
                    image.allow_stretch = True
                    image.size_hint = None, None
                    self.root.add_widget(image, index=1)
        except Exception, e:
            self.obstacle_list = {"obstacle_list":[]}

    def on_touch_down(self, touch):

        if main_page.current_obstacle == {}:
            return


        x, y = touch.pos
        image = Image(source = main_page.icon_dir + main_page.current_obstacle['Image'], size=main_page.current_obstacle['Initial_Size'][:2])
        image.center_x = touch.pos[0]
        image.center_y = touch.pos[1]
        image.size_hint = None, None
        image.allow_stretch = True
        if self.root.pos[0] + image.width/2 <= x and x <= self.root.pos[0] + self.root.size[0] - image.width/2:
            if self.root.pos[1] + image.height/2 <= y and y <= self.root.pos[1] + self.root.size[1] - image.height/2:
                if collision_detect(self.obstacle_list, main_page.current_obstacle, touch.pos)[0]:
                    self.root.add_widget(image, index=1)
                    obstacle = {}
                    obstacle['title'] = main_page.current_obstacle['Name']
                    obstacle['position'] = touch.pos
                    obstacle['size'] = main_page.current_obstacle['Initial_Size']
                    obstacle['image'] = main_page.current_obstacle['Image']
                    self.obstacle_list['obstacle_list'].append(obstacle)
                    with open(main_page.file_dir + main_page.file_name, 'w') as f:
                        json.dump(self.obstacle_list, f)
                else:
                    print collision_detect(self.obstacle_list, main_page.current_obstacle, touch.pos)
                    label = Label(text="Clicked", pos = touch.pos, color=(0, 0, 0, 1))
                    self.root.add_widget(label)

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