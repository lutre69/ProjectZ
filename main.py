# coding: utf8
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen


class Skill(object):
    def __init__(self, skill_id, **kwargs):
        self.skill_id = skill_id
        self.set_name = kwargs.get('set_name')
        self.title = kwargs.get('title')
        self.summary = kwargs.get('summary')


class Student(object):
    def __init__(self, student_id, **kwargs):
        self.id_ = student_id
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.class_ = kwargs.get('class')


class CustomDropDown(DropDown):
    pass


class StandardButton(Button):
    pass


class SkillsScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class SkillsPopupLayout(GridLayout):
    def __init__(self, app, skills_list, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.skills_list = skills_list
        self.btn_dict = {}
        for s in self.skills_list:
            button = Button(text=s.title)
            self.add_widget(button)
            button.bind(on_release=self.select)
            self.btn_dict[button] = s

    def select(self, obj):
        self.app.selected_skill = self.btn_dict[obj]
        self.parent.parent.parent.dismiss()


class StudentPopupLayout(GridLayout):
    def __init__(self, app, student_list, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.student_list = student_list
        self.btn_dict = {}
        for s in self.student_list:
            button = Button(text="{} {}".format(s.surname, s.name))
            self.add_widget(button)
            button.bind(on_release=self.select)
            self.btn_dict[button] = s

    def select(self, obj):
        self.app.selected_student = self.btn_dict[obj]
        self.parent.parent.parent.dismiss()


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
                button = Button(text=x, size_hint_y=None, height="44dp",
                                background_color=[1, 1, 1, 0.6])
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
    selected_student = ObjectProperty()
    selected_skill = ObjectProperty()

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

    def open_student_popup(self):
        Popup(content=StudentPopupLayout(self,
              self.student_list,
              cols=2),
              title='Faites votre choix',
              auto_dismiss=False).open()

    def on_selected_student(self, instance, student):
        self.root.skills_screen.student_name.text = "{} {}".format(student.surname,
                                                                   student.name)

    def open_skills_popup(self):
        Popup(content=SkillsPopupLayout(cols=2,
              skills_list=self.skills_list,
              app=self),
              title='Faites votre choix',
              size_hint_y=0.5).open()

    def on_selected_skill(self, instance, skill):
        self.root.skills_screen.skill_name.text = skill.title
        self.root.skills_screen.skill_summary.text = skill.summary

    def set_student_skill(self, value):
        try:
            student = self.selected_student.id_
            output = self.data_output
            skill = self.selected_skill.title
            try:
                length = len(output[student][skill])
                output[student][skill][length] = value
            except KeyError:
                try:
                    output[student][skill] = {0: value}
                except KeyError:
                    output[student] = self.students_data[student]
            output._is_changed = True
            output.store_sync()
        except AttributeError:
            pass

    def on_pause(self):
        return True


if __name__ == '__main__':
    ProjectZApp().run()
