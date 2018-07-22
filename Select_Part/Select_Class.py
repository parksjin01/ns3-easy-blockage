from kivy.uix.listview import ListView, ListItemButton
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.label import Label
from kivy.uix.image import Image

import json

import main_page

# TODO
# 1. Resizing initial leg number and size
# 2. Delete description and pop-up description when mouse on the widget

class MyLabel(GridLayout):
    def __init__(self):
        super(MyLabel, self).__init__()

    def setting(self, kwargs):

        self.rows = 6

        self.padding = [20, 0, 0, 0]

        self.add_widget(Label(text=" ", text_size = kwargs['Name'].size), index=2)
        self.add_widget(Label(text=" ", text_size = kwargs['Name'].size))
        kwargs['Name'].text_size = (int(kwargs['Name'].size[0] * 2), kwargs['Name'].size[1])
        self.add_widget(kwargs['Name'], index=1)
        self.add_widget(Label(text=" ", text_size = kwargs['Name'].size))
        # self.add_widget(kwargs['Description'], index=2)
        inner_layout = GridLayout()
        inner_layout.cols = 2
        inner_layout.add_widget(kwargs['Size'], index=0)
        inner_layout.add_widget(kwargs['Initial_Legs'], index=1)
        # self.add_widget(kwargs['Size'], index=3)
        self.add_widget(inner_layout, index=1)


class SelectItem(GridLayout, ListItemButton):
    def __init__(self, **kwargs):
        super(SelectItem, self).__init__(**kwargs)

        labels = {}
        for key, value in kwargs.items():
            if key != 'height' and key != 'index' and key != 'Image':
                labels[key] = Label(text=value, markup = True)

        label_set = MyLabel()
        label_set.setting(labels)

        self.cols = 2
        self.height = kwargs['height']
        self.background_color = (.7, .7, .7, 1)
        self.deselected_color = (.7, .7, .7, 1)
        self.selected_color = (0.3, 0.3, 0.3, 1)
        # labels['Image'].pos = (self.width / 4 * 3, self.height / 10 * 4)
        self.padding = [10, 0, 0, 0]
        self.add_widget(Image(source=main_page.icon_dir + kwargs['Image']))
        self.add_widget(label_set)

class SelectList(ListView):
    def __init__(self, **kargs):
        with open('Select_Part/Obstacles.json', 'r') as f:
            self.data = json.load(f)
            main_page.total_obstacle = self.data
        super(SelectList, self).__init__(**kargs)
        blockage_item = ListAdapter(data=self.data['Obstacles'], args_converter=self.args_converter, cls = SelectItem, selection_mode="single", allow_empty_selection="True")
        self.adapter = blockage_item
        self.adapter.bind(on_selection_change=self.selection_change)

    def selection_change(self, adapter, *args):
        try:
            key = adapter.selection[0].children[0].children[3].text
            for obstacle in main_page.total_obstacle['Obstacles']:
                if '[b][size=40]'+obstacle['Name']+'[/size][/b]' == key:
                    main_page.current_obstacle = obstacle
                    break

        except:
            pass

    def args_converter(self, row_index, obj):
        return {
            'Name': '[b][size=40]'+obj['Name']+'[/size][/b]',
            'Description': obj['Description'],
            'Size': '[size=20]' + ' '.join(map(str, obj['Initial_Size'])) + '[/size]',
            'Initial_Legs': '[size=20]' + str(obj['Initial_Legs']) + '[/size]',
            'Image': obj['Image'],
            'height': 130
        }

