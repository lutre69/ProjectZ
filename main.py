# coding: utf8
from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.storage.jsonstore import JsonStore
from properties import Student, Skill
from root import Root


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
