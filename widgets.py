from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class MenuButton(Button):
    drop_down = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_down = DropDown()
        self.update_menu(self.drop_down, 'Accueil',
                         ['Evaluation', 'Comportement'])
        self.bind(on_release=self.drop_down.open)

    def update_menu(self, instance, value, screen_list):
        setattr(self, 'text', value)
        instance.clear_widgets()
        for x in screen_list:
            if x != value:
                button = DropButton(text=x)
                button.bind(on_release=lambda btn: instance.select(btn.text))
                instance.add_widget(button)
                button.canvas.ask_update()


class DropButton(Button):
    pass


class SkillLabel(BoxLayout):
    pass
