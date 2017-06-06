# coding: utf8
import os
import json
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.storage.jsonstore import JsonStore
from kivy.uix.label import Label
from data_obj import Skill, Student
from root import Root


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

    def on_pause(self):
        return True


if __name__ == '__main__':
    ProjectZApp().run()
