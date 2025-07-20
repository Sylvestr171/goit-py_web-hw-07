from db_connection import session
from models import Teachers, Groups, Student, Subjects, Grades
from generetor import groups, students, teachers, subjects, grades
from random import choice

groups_db = [Groups(name=ithem.name) for ithem in groups]
session.add_all(groups_db)
teachers_db = [Teachers(fullname=ithem.name, email=ithem.email) for ithem in teachers]
session.add_all(teachers_db)
session.commit()

students_db = [Student(fullname=ithem.name, group_id=choice(groups_db).id) for ithem in students]
session.add_all(students_db)
subjects_db = [Subjects(name=ithem.name, teacher_id=choice(teachers_db).id) for ithem in subjects]
session.add_all(subjects_db)
session.commit()

def students_id_check(students_db,name):
    for i in students_db:
        if i.fullname == name:
            return i.id

def subject_id_check(subjects_db, name):
    for i in subjects_db:
        if i.name == str(name):
            return i.id

grades_db = [Grades(grade=ithem.grade, grade_date=ithem.grade_date, student_id=students_id_check(students_db, ithem.student_name), subject_id=subject_id_check(subjects_db, ithem.subject_name)) for ithem in grades]
session.add_all(grades_db)
session.commit()