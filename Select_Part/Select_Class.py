from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label

import json

import main_page

# TODO
# 1. Add proper picture for each obstacles
# 2. Resizing initial leg number and size
# 3. Delete description and pop-up description when mouse on the widget

class MyLabel(GridLayout):
    def __init__(self):
        super(MyLabel, self).__init__()

    def setting(self, kwargs):

        self.rows = len(kwargs)

        self.add_widget(kwargs['Name'], index=1)
        self.add_widget(kwargs['Description'], index=2)
        self.add_widget(kwargs['Size'], index=3)
        self.add_widget(kwargs['Initial_Legs'], index=4)


class SelectItem(GridLayout, ListItemButton):
    def __init__(self, **kwargs):
        super(SelectItem, self).__init__(**kwargs)

        labels = {}
        for key, value in kwargs.items():
            if key != 'height' and key != 'index':
                labels[key] = Label(text=value)

        label_set = MyLabel()
        label_set.setting(labels)

        self.cols = 2
        self.height = kwargs['height']
        # labels['Image'].pos = (self.width / 4 * 3, self.height / 10 * 4)
        labels['Image'].width = 30
        self.add_widget(labels['Image'])
        self.add_widget(label_set)

class SelectList(ListView):
    def __init__(self, **kargs):
        with open('Select_Part/Obstacles.json', 'r') as f:
            self.data = json.load(f)
        super(SelectList, self).__init__(**kargs)
        blockage_item = ListAdapter(data=self.data['Obstacles'], args_converter=self.args_converter, cls = SelectItem, selection_mode="single", allow_empty_selection="True")
        self.adapter = blockage_item
        self.adapter.bind(on_selection_change=self.selection_change)

    def selection_change(self, adapter, *args):
        main_page.current_obstacle = adapter.selection[0].children[0].children[0].text

    def args_converter(self, row_index, obj):
        return {
            'Name': obj['Name'],
            'Description': obj['Description'],
            'Size': ' '.join(map(str, obj['Initial_Size'])),
            'Initial_Legs': str(obj['Initial_Legs']),
            'Image': obj['Image'],
            'height': 150
        }

