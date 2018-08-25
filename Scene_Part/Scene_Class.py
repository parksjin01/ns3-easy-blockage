from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
import json
import math
import main_page
import hashlib

NUM_MENU = 4
MENU_FUNC = []
MENU_NAME = ["Delete", "Delete", "Delete", "Delete"]
OBSTACLE_IMAGE = {}

def distance(point1, point2):
    dist = 0
    if len(point1) == len(point2):
        for idx in range(len(point1)):
            dist += (point1[idx] - point2[idx])**2
    return math.sqrt(dist)

def collision_detect(obstacle_list, current_obstacle, pos):
    if obstacle_list == {}:
        return True, {}
    for obstacle in obstacle_list['obstacle_list']:
        tmp_widget = OBSTACLE_IMAGE[obstacle['id']]
        if tmp_widget.pos[0] - current_obstacle.size[0]/2 <= pos[0] and pos[0] <= tmp_widget.pos[0] + tmp_widget.size[0] + current_obstacle.size[0]/2 and tmp_widget.pos[1] - current_obstacle.size[1]/2 <= pos[1] and pos[1] <= tmp_widget.pos[1] + tmp_widget.size[1] + current_obstacle.size[1]/2:
            return False, obstacle

    return True, {}

def check_button_clicked(widget, btn_list, pos):
    btn_clicked = False

    if type(btn_list) == type([]):
        for btn in btn_list:
            if btn.pos[0] <= pos[0] and pos[0] <= btn.pos[0] + btn.size[0] and btn.pos[1] <= pos[1] and pos[1] <= btn.pos[1] + btn.size[1]:
                btn_clicked = True

                obstacle_id, button_id = btn.id.split(",")
                if button_id == "0":
                    delete_obstacle(widget, obstacle_id)

                break
    return btn_clicked

def delete_obstacle(widget, id):
    with open(main_page.file_dir + main_page.file_name, "r") as f:
        obstacle_list = json.load(f)
        for obstacle in obstacle_list["obstacle_list"]:
            if obstacle['id'] == id:
                obstacle_list["obstacle_list"].remove(obstacle)
                break

    with open(main_page.file_dir + main_page.file_name, 'w') as f:
        json.dump(obstacle_list, f)

    widget.remove_widget(OBSTACLE_IMAGE[id])

class Touch_Handle():
    def __init__(self, scatter, root):
        self.scatter = scatter
        self.root = root
        self.current_popup_menu = 0
        try:
            with open(main_page.file_dir + main_page.file_name, 'r') as f:
                self.obstacle_list = json.load(f)
                for obstacle in self.obstacle_list['obstacle_list']:
                    image = Image(source=main_page.icon_dir + obstacle['image'], size=obstacle['size'][:2])
                    image.center_x = obstacle['position'][0]
                    image.center_y = obstacle['position'][1]
                    image.allow_stretch = True
                    image.size_hint = None, None
                    self.scatter.add_widget(image, index=1)

                    OBSTACLE_IMAGE[obstacle['id']] = image
        except Exception, e:
            self.obstacle_list = {"obstacle_list":[]}
        print self.root.children

    def on_touch_down(self, touch):

        print "TOUCH", touch.pos

        if main_page.current_obstacle == {}:
            return


        x, y = touch.pos
        image = Image(source = main_page.icon_dir + main_page.current_obstacle['Image'], size=main_page.current_obstacle['Initial_Size'][:2])
        image.center_x = touch.pos[0]
        image.center_y = touch.pos[1]
        image.size_hint = None, None
        image.allow_stretch = True
        print type(self.root)
        print self.root.pos, self.root.size
        if self.root.pos[0] + image.width/2 <= x and x <= self.root.pos[0] + self.root.size[0] - image.width/2:
            if self.root.pos[1] + image.height/2 <= y and y <= self.root.pos[1] + self.root.size[1] - image.height/2:
                not_collision, collide_obstacle = collision_detect(self.obstacle_list, image, touch.pos)

                if check_button_clicked(self.root, self.current_popup_menu, touch.pos):
                    if self.current_popup_menu != 0:
                        for item in self.current_popup_menu:
                            self.root.remove_widget(item)
                        self.current_popup_menu = 0

                elif not_collision:
                    if self.current_popup_menu != 0:
                        for item in self.current_popup_menu:
                            self.root.remove_widget(item)
                        self.current_popup_menu = 0

                    self.scatter.add_widget(image, index=1)
                    obstacle = {}
                    obstacle['title'] = main_page.current_obstacle['Name']
                    obstacle['position'] = touch.pos
                    obstacle['size'] = main_page.current_obstacle['Initial_Size']
                    obstacle['image'] = main_page.current_obstacle['Image']
                    obstacle['id'] = hashlib.sha256(str(touch.pos[0]) + str(touch.pos[1])).hexdigest()
                    OBSTACLE_IMAGE[obstacle['id']] = image
                    self.obstacle_list['obstacle_list'].append(obstacle)
                    with open(main_page.file_dir + main_page.file_name, 'w') as f:
                        json.dump(self.obstacle_list, f)

                else:
                        if self.current_popup_menu != 0:
                            for item in self.current_popup_menu:
                                self.root.remove_widget(item)
                            self.current_popup_menu = 0

                        menu = []

                        for idx in range(NUM_MENU):
                            tmp_btn = Button(text="Delete", background_color=(0x81, 0xd4, 0xfa), size_hint=(.1, .1))
                            tmp_btn.pos = [touch.pos[0], touch.pos[1] - tmp_btn.size[1] - idx * tmp_btn.size[1]]
                            tmp_btn.id = collide_obstacle['id'] + "," + str(idx)
                            print tmp_btn.id
                            menu.append(tmp_btn)
                        self.current_popup_menu = menu

                        for item in menu:
                            self.root.add_widget(item)

    def on_touch_move(self, touch):
        print touch

class Scene(Widget):
    def __init__(self, **kwargs):
        super(Scene, self).__init__(**kwargs)
        scatter = Scatter()
        scatter.size = self.size
        scatter.scale = 1
        self.add_widget(scatter)
        scatter.add_widget(Label(text='Hello world', pos = (664, 758), color = (0, 0, 0, 1)))
        # w = Widget()
        # w.size = self.size
        self.touch_handle = Touch_Handle(scatter, self)
        # self.pos_hint = (.25, .0)
        # self.size_hint = (.5, .9)
        # self.center_x =
    def on_touch_down(self, touch):
        self.touch_handle.on_touch_down(touch)

    def on_touch_move(self, touch):
        self.touch_handle.on_touch_move(touch)