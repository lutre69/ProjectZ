from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.popup import Popup
from popups import ChoicePopup
from functools import partial


class Root(BoxLayout):
    _selected_class = ObjectProperty()
    _selected_skill_set = ObjectProperty()
    active_students = ListProperty()
    active_skills = ListProperty()
    choice_popup = ObjectProperty()

    def __init__(self, students, classes, skills, skill_sets, **kwargs):
        super().__init__(**kwargs)
        self.student_list = students
        self.class_list = classes
        self.skill_list = skills
        self.skill_set_list = skill_sets
        self.selected_class = self.class_list[0]
        self.selected_skill_set = self.skill_set_list[0]
        self.screen_list = ['Accueil', 'Evaluation', 'Comportement']
        self.menu.drop_down.bind(on_select=self.select_screen)

    @property
    def selected_class(self):
        return self._selected_class

    @selected_class.setter
    def selected_class(self, value):
        self.active_students = [s for s in self.student_list
                                if s.class_ == value.class_]
        self.start_screen.active_class_label.text = "Classe : {}".format(value.class_)
        self._selected_class = value

    @property
    def selected_skill_set(self):
        return self._selected_skill_set

    @selected_skill_set.setter
    def selected_skill_set(self, value):
        self.active_skills = [s for s in self.skill_list
                              if s.set_name == value.set_name]
        self.start_screen.active_skill_set_label.text = "Competences : {}".format(value.set_name)
        self._selected_skill_set = value

    def _on_choice(self, item, attribute, item_list, callback,
                   popup_inst, choice, btn_inst):
        self.choice_popup.dismiss()
        for x in item_list:
            if getattr(x, attribute) == choice:
                item = x
        return callback(item)

    def select_screen(self, instance, value):
        self.screen_manager.current = value
        self.menu.update_menu(instance, value, self.screen_list)

    def open_choice_popup(self, item, item_list, attribute, callback,
                          title='Choisissez', size_hint_y=None):
        labels = [getattr(x, attribute) for x in item_list]
        content = ChoicePopup(labels=labels)
        __on_choice = partial(self._on_choice, item, attribute,
                              item_list, callback)
        content.bind(on_choice=__on_choice)
        self.choice_popup = Popup(title=title, content=content,
                                  size_hint_y=size_hint_y, auto_dismiss=False)
        self.choice_popup.open()

    def clear_display_label(self):
        self.start_screen.display_label.clear_widgets()
        self.start_screen.display_header.clear_widgets()
