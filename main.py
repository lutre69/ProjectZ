# coding: utf8
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button


class Skill(object):
    def __init__(self, skill_id, **kwargs):
        self.skill_id = skill_id
        self.set_name = kwargs.get('set_name')
        self.title = kwargs.get('title')
        self.summary = kwargs.get('summary')


class Student(object):
    def __init__(self, student_id, **kwargs):
        self.student_id = student_id
        self.student_name = kwargs.get('name')
        self.student_surname = kwargs.get('surname')
        self.student_class = kwargs.get('class')


class CustomDropDown(DropDown):
    pass


class StandardButton(Button):
    pass


class MenuButton(Button):
    drop_down = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.drop_down = CustomDropDown()
        self.bind(on_release=self.drop_down.open)

    def update_menu(self, instance, value, screen_list):
        setattr(self, 'text', value)
        instance.clear_widgets()
        for x in screen_list:
            if x != value:
                button = Button(text=x, size_hint_y=None, height="44dp")
                button.bind(on_release=lambda btn: instance.select(btn.text))
                instance.add_widget(button)


class Root(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_list = ['Accueil', 'Evaluation', 'Comportement']
        self.menu.drop_down.bind(on_select=self.select_screen)

    def select_screen(self, instance, value):
        self.screen_manager.current = value
        self.menu.update_menu(instance, value, self.screen_list)


class ProjectZApp(App):
    students_data = ObjectProperty(JsonStore('data/students.json'))
    skills_data = ObjectProperty(JsonStore('data/skills.json'))
    data_output = ObjectProperty(JsonStore('data/outputs.json'))
    student_list = ListProperty()
    skills_list = ListProperty()

    def build(self):
        self.student_list = self.get_students()
        self.skills_list = self.get_skills()
        self.root = Root()
        return self.root

    def get_students(self):
        data = self.students_data
        return [Student(id_, **data[id_]) for id_ in data]

    def get_skills(self):
        data = self.skills_data
        return [Skill(id_, **data[id_]) for id_ in data]

    def export_data(self, data, file='export.txt'):
        path = '/'.join([self.user_data_dir, file])
        with open(path, 'w') as file:
            file.write(data)
            file.close()
        return path

    def on_pause(self):
        return True


if __name__ == '__main__':
    ProjectZApp().run()
