from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from popups import ConfirmPopup
from functools import partial
import time


class StartScreen(Screen):
    app_obj = ObjectProperty()
    root_obj = ObjectProperty()

    def open_class_popup(self):
        root = self.root_obj
        args = {'item': root.selected_class, 'item_list': root.class_list,
                'attribute': 'class_', 'callback': self.select_class,
                'title': 'Choisissez une classe', 'size_hint_y': 0.3}
        return root.open_choice_popup(**args)

    def select_class(self, a_class):
        self.active_class_label.text = "{}".format(a_class.class_)
        self.root_obj.selected_class = a_class

    def open_skill_set_popup(self):
        args = {'item': self.root_obj.selected_skill_set,
                'item_list': self.root_obj.skill_set_list,
                'attribute': 'set_name',
                'callback': self.select_skill_set,
                'title': 'Choisissez un jeu de compétences',
                'size_hint_y': 0.3}
        return self.root_obj.open_choice_popup(**args)

    def select_skill_set(self, a_set):
        self.active_skill_set_label.text = "{}".format(a_set.set_name)
        self.root_obj.selected_skill_set = a_set

    def display_behaviour(self):
        self.display_header.clear_widgets()
        self.display_label.clear_widgets()
        output = self.app_obj.data_output
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
        self.display_header.add_widget(header_layout)
        self.display_label.add_widget(grid_layout)

    def display_skills(self):
        self.display_header.clear_widgets()
        self.display_label.clear_widgets()
        output = self.app_obj.data_output
        data = {}
        header = ["prenom"]
        header.extend([skill.title for skill in self.root_obj.active_skills])
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
        self.display_header.add_widget(header_layout)
        self.display_label.add_widget(grid_layout)


class SkillsScreen(Screen):
    root_obj = ObjectProperty()
    app_obj = ObjectProperty()
    selected_student = ObjectProperty()
    selected_skill = ObjectProperty()
    student_review = ObjectProperty(GridLayout())
    confirm_popup = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(selected_student=self.display_stud_skills)
        self.bind(selected_skill=self.display_stud_skills)

    def open_student_popup(self):
        args = {'item': self.selected_student,
                'item_list': self.root_obj.active_students,
                'attribute': 'surname',
                'callback': self.select_student,
                'title': 'Choisissez un élève',
                'size_hint_y': 1}
        return self.root_obj.open_choice_popup(**args)

    def _on_answer(self, func, instance, answer):
        self.confirm_popup.dismiss()
        if answer == 'yes':
            return func()
        else:
            return

    def select_student(self, student):
        self.student_name.text = "{} {}".format(student.surname,
                                                student.name)
        self.selected_student = student

    def select_skill(self, skill):
        self.skill_name.text = skill.title
        self.skill_summary.text = skill.summary
        self.selected_skill = skill

    def open_skills_popup(self):
        args = {'item': self.selected_skill,
                'item_list': self.root_obj.active_skills,
                'attribute': 'title',
                'callback': self.select_skill,
                'title': 'Choisissez une compétence',
                'size_hint_y': 0.4}
        return self.root_obj.open_choice_popup(**args)

    def pre_set_student_skill(self, value):
        try:
            skill = self.selected_skill.title
            student = self.selected_student
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
        student = self.selected_student.id_
        output = self.app_obj.data_output
        skill = self.selected_skill.title
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

    def display_stud_skills(self, *ignore):
        try:
            assert self.selected_student and self.selected_skill
            self.student_review.add_widget(Label(text='caca',
                                                 size_hint_y=.8))
        except AssertionError:
            pass


class BehaviourScreen(Screen):
    app_obj = ObjectProperty()
    root_obj = ObjectProperty()
    selected_student = ObjectProperty()
    confirm_popup = ObjectProperty()

    def open_student_popup(self):
        args = {'item': self.selected_student,
                'item_list': self.root_obj.active_students,
                'attribute': 'surname',
                'callback': self.select_student,
                'title': 'Choisissez un élève',
                'size_hint_y': 1}
        return self.root_obj.open_choice_popup(**args)

    def select_student(self, student):
        self.student_name.text = "{} {}".format(student.surname,
                                                student.name)
        self.selected_student = student

    def _on_answer(self, func, instance, answer):
        self.confirm_popup.dismiss()
        if answer == 'yes':
            return func()
        else:
            return

    def pre_set_student_disobedience(self, value):
        try:
            student = self.selected_student
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
        student = self.selected_student.id_
        output = self.app_obj.data_output
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
