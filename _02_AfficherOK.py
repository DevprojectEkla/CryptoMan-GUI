from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup


class CustomPopup:
    """En chantier: apparemment pas utilisé, remplacé par Mypopup dans le fichier .kv"""

    pop_layout = ObjectProperty()
    button_list = ListProperty()
    b_number = NumericProperty()
    b_text = ListProperty()
    b_size = ListProperty()
    b_width = ListProperty()
    b_height = ListProperty()
    label = ObjectProperty()
    label_text = StringProperty()
    popup = ObjectProperty()
    pop_title = StringProperty()
    pop_content = ObjectProperty()
    pop_size = NumericProperty()

    def initPopup(self):
        self.button_list = []
        if self.pop_layout is None:
            self.pop_layout = GridLayout(cols=1)
        self.pop_content = self.pop_layout
        for i in range(self.b_number):
            button = Button(text=self.b_text[i], size_hint_y=None, height=40)
            self.button_list.append(button)
            self.pop_content.add_widget(button)

        self.pop_content.add_widget(self.label(text=self.label_text))

        self.popup = Popup(title=self.pop_title,
                           content=self.pop_content, size_hint=self.pop_size)
        self.button_list[0].bind(on_release=self.popup.dismiss)
        self.popup.open()
