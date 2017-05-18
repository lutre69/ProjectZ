# coding: utf8


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

