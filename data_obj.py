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
        self.skills_dict = {}
