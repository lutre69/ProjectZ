from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty, ListProperty
from kivy.uix.button import Button
from functools import partial


class ConfirmPopup(GridLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        self.register_event_type('on_answer')
        super().__init__(**kwargs)

    def on_answer(self, *args):
        pass


class ChoicePopup(GridLayout):
    labels = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_choice')
        for x in self.labels:
            dispatch = partial(self.dispatch, 'on_choice', x)
            self.add_widget(Button(text=x,
                                   on_release=dispatch))

    def on_choice(self, *args):
        pass
