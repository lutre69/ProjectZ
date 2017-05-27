# coding: utf8
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from functools import partial
import time
import os
import json


class SkillSet:
    def __init__(self, set_name=None):
        self.set_name = set_name


class Skill:
    def __init__(self, skill_id, **kwargs):
        self.skill_id = skill_id
        self.title = kwargs.get('title')
        self.summary = kwargs.get('summary')
        self.set_name = kwargs.get('set_name')
        self.skill_set_obj = SkillSet(set_name=self.set_name)


class Class:
    def __init__(self, class_=None):
        self.class_ = class_


class Student:
    def __init__(self, student_id, **kwargs):
        self.id_ = student_id
        self.name = kwargs.get('name')
        self.surname = kwargs.get('surname')
        self.class_ = kwargs.get('class')
        self.class_obj = Class(class_=self.class_)


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


class Root(BoxLayout):
    selected_student = ObjectProperty()
    selected_skill = ObjectProperty()
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

    def open_class_popup(self):
        return self.open_choice_popup(item=self.selected_class,
                                      item_list=self.class_list,
                                      attribute='class_',
                                      callback=self.select_class,
                                      title='Choisissez une classe',
                                      size_hint_y=0.3)

    def open_skill_set_popup(self):
        return self.open_choice_popup(item=self.selected_skill_set,
                                      item_list=self.skill_set_list,
                                      attribute='set_name',
                                      callback=self.select_skill_set,
                                      title='Choisissez un jeu de compétences',
                                      size_hint_y=0.3)

    def open_student_popup(self):
        return self.open_choice_popup(item=self.selected_student,
                                      item_list=self.active_students,
                                      attribute='surname',
                                      callback=self.select_student,
                                      title='Choisissez un élève',
                                      size_hint_y=1)

    def open_skills_popup(self):
        return self.open_choice_popup(item=self.selected_skill,
                                      item_list=self.active_skills,
                                      attribute='title',
                                      callback=self.select_skill,
                                      title='Choisissez une compétence',
                                      size_hint_y=0.4)

    def select_class(self, a_class):
        self.start_screen.active_class_label.text = "{}".format(a_class.class_)
        self.selected_class = a_class

    def select_skill_set(self, a_set):
        self.start_screen.active_skill_set_label.text = "{}".format(a_set.set_name)
        self.selected_skill_set = a_set

    def select_student(self, student):
        self.skills_screen.student_name.text = "{} {}".format(student.surname,
                                                              student.name)
        self.behaviour_screen.student_name.text = "{} {}".format(student.surname,
                                                                 student.name)
        self.selected_student = student

    def select_skill(self, skill):
        self.skills_screen.skill_name.text = skill.title
        self.skills_screen.skill_summary.text = skill.summary
        self.selected_skill = skill

    def clear_display_label(self):
        self.start_screen.display_label.clear_widgets()
        self.start_screen.display_header.clear_widgets()


class ProjectZApp(App):
    students_data = ObjectProperty(JsonStore('data/students.json'))
    skills_data = ObjectProperty(JsonStore('data/skills.json'))
    data_output = ObjectProperty(JsonStore('data/outputs.json'))
    confirm_popup = ObjectProperty()

    def build(self):
        students, classes = self.get_students()
        skills, skill_sets = self.get_skills()
        self.root = Root(students, classes, skills, skill_sets)
        return self.root

    def get_students(self):
        data = self.students_data
        students = [Student(id_, **data[id_]) for id_ in data]
        temp_list, classes = [], []
        for s in students:
            if s.class_obj.class_ in temp_list:
                pass
            else:
                temp_list.append(s.class_obj.class_)
                classes.append(s.class_obj)
        students.sort(key=lambda x: x.surname)
        return students, classes

    def get_skills(self):
        data = self.skills_data
        skills = [Skill(id_, **data[id_]) for id_ in data]
        temp_list, skill_sets = [], []
        for s in skills:
            if s.skill_set_obj.set_name in temp_list:
                pass
            else:
                temp_list.append(s.skill_set_obj.set_name)
                skill_sets.append(s.skill_set_obj)
        return skills, skill_sets

    def export_data(self, i=0):
        self.root.start_screen.display_header.clear_widgets()
        self.root.start_screen.display_label.clear_widgets()
        file = 'export_{}'.format(i)
        data = {key: self.data_output[key] for key in self.data_output}
        path = '/'.join([self.user_data_dir, file])
        if os.path.isfile(path):
            i += 1
            self.export_data(i)
        else:
            with open(path, 'w') as file:
                json.dump(data, file)
                file.close()
            label = Label(text="Votre fichier a été exporté avec\n"
                          "Succès, il est situé en :\n{}\nLes données du"
                          "téléphone ont été effacées".format(path))
            self.root.start_screen.display_label.add_widget(label)
            list_keys = {i: key for key in self.data_output}
            [self.data_output.store_delete(key) for i, key in list_keys.items()]
            self.data_output._is_changed = True
            self.data_output.store_sync()

    def _on_answer(self, func, instance, answer):
        self.confirm_popup.dismiss()
        if answer == 'yes':
            return func()
        else:
            return

    def pre_set_student_skill(self, value):
        try:
            skill = self.root.selected_skill.title
            student = self.root.selected_student
            content = ConfirmPopup(text="Confirmez la note:\n\n{} {}\n\n"
                                        "{} {}".format(
                                         skill, value, student.surname,
                                         student.name))
            func = partial(self.set_student_skill, value)
            __on_answer = partial(self._on_answer, func)
            content.bind(on_answer=__on_answer)
            self.confirm_popup = Popup(title="Confirmation",
                                       content=content,
                                       size_hint_y=.4,
                                       auto_dismiss=False)
            self.confirm_popup.open()
        except AttributeError:
            pass

    def set_student_skill(self, value):
        student = self.root.selected_student.id_
        output = self.data_output
        skill = self.root.selected_skill.title
        try:
            length = len(output[student][skill])
            output[student][skill][length] = value
        except KeyError:
            try:
                output[student][skill] = {0: value}
            except KeyError:
                output[student] = self.students_data[student]
                output[student][skill] = {0: value}
        output._is_changed = True
        output.store_sync()

    def display_skills(self):
        self.root.start_screen.display_header.clear_widgets()
        self.root.start_screen.display_label.clear_widgets()
        output = self.data_output
        data = {}
        header = ["prenom"]
        header.extend([skill.title for skill in self.root.active_skills])
        header_layout = GridLayout(cols=len(header))
        [header_layout.add_widget(Label(text=item,
                                        font_size='12sp')) for item in header]
        grid_layout = GridLayout(cols=len(header), size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        for key in output:
            data[key] = output[key]
            try:
                data[key].pop('class')
                data[key].pop('name')
            except KeyError:
                pass
            row = [data[key]["surname"]]
            for skill in header[1:]:
                try:
                    item = data[key][skill]
                    row.append(", ".join(str(item[i]) for i in item))
                except KeyError:
                    row.extend([" "])
            [grid_layout.add_widget(Label(text=item, size_hint_y=None,
                                          height='40dp',
                                          font_size='12sp')) for item in row]
        for label in header_layout.children:
            if label.text != "prenom":
                label.text = label.text[:4]
        self.root.start_screen.display_header.add_widget(header_layout)
        self.root.start_screen.display_label.add_widget(grid_layout)

    def pre_set_student_disobedience(self, value):
        try:
            student = self.root.selected_student
            content = ConfirmPopup(text="Confirmez la sanction:\n\n{}\n\n"
                                        "{} {}".format(
                                         value, student.surname,
                                         student.name))
            func = partial(self.set_student_disobedience, value)
            __on_answer = partial(self._on_answer, func)
            content.bind(on_answer=__on_answer)
            self.confirm_popup = Popup(title="Confirmation",
                                       content=content,
                                       size_hint_y=.4,
                                       auto_dismiss=False)
            self.confirm_popup.open()
        except AttributeError:
            pass

    def set_student_disobedience(self, value):
        time_ = time.strftime("%d %B %H:%M:%S")
        student = self.root.selected_student.id_
        output = self.data_output
        try:
            length = len(output[student][value])
            output[student][value][length] = time_
        except KeyError:
            try:
                output[student][value] = {0: time_}
            except KeyError:
                output[student] = self.students_data[student]
                output[student][value] = {0: time_}
        output._is_changed = True
        output.store_sync()

    def display_behaviour(self):
        self.root.start_screen.display_header.clear_widgets()
        self.root.start_screen.display_label.clear_widgets()
        output = self.data_output
        data = {}
        header = ["prenom",
                  "Bavardage", "Insolence", "Inactivite", "Travail non fait"]
        header_layout = GridLayout(cols=len(header))
        [header_layout.add_widget(Label(text=item,
                                        font_size='12sp')) for item in header]
        grid_layout = GridLayout(cols=len(header), size_hint_y=None)
        grid_layout.bind(minimum_height=grid_layout.setter('height'))
        for key in output:
            data[key] = output[key]
            try:
                data[key].pop('class')
                data[key].pop('name')
            except KeyError:
                pass
            row = [data[key]["surname"]]
            for behaviour in header[1:]:
                try:
                    item = data[key][behaviour]
                    row.append("\n".join(str(item[i]) for i in item))
                except KeyError:
                    row.extend([" "])
            [grid_layout.add_widget(Label(text=item, size_hint_y=None,
                                          height='40dp',
                                          font_size='12sp')) for item in row]
        for label in header_layout.children:
            if label.text != "prenom":
                label.text = label.text[:4]
        self.root.start_screen.display_header.add_widget(header_layout)
        self.root.start_screen.display_label.add_widget(grid_layout)

    def on_pause(self):
        return True


if __name__ == '__main__':
    ProjectZApp().run()
