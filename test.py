from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivymd.theming import ThemeManager


class CustomLabel(Label):

    def on_touch_down(self, touch):
        print("\nCustomLabel.on_touch_down:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]
            return True
        return super(CustomLabel, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        print("\nCustomLabel.on_touch_move:")

        if self.collide_point(*touch.pos):
            print("\ttouch.pos =", touch.pos)
            Window.top = self.touch_y + touch.spos[0]
            Window.left = self.touch_x + touch.spos[1]
            return True
        return super(CustomLabel, self).on_touch_move(touch)


class CustBoxLayout(BoxLayout):
    pass


class TestApp(App):
    theme_cls = ThemeManager()

    def build(self):
        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Purple'

        return CustBoxLayout()


if __name__ == "__main__":
    TestApp().run()