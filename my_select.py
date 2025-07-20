from db_connection import session
from sqlalchemy import func, desc
from models import Teachers, Groups, Student, Subjects, Grades

# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
# SELECT AVG(grades.grade) as avarage_grades, students.fullname 
# FROM grades 
# JOIN students ON students.id=grades.student_id 
# GROUP BY grades.student_id, students.fullname 
# order by avarage_grades desc limit 5
def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grades.grade), 2).label('avg_grade'))\
        .select_from(Grades).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

# Знайти студента із найвищим середнім балом з певного предмета.
# SELECT MAX(avg_grade), students.fullname 
# from (select AVG(grades.grade) as avg_grade 
# FROM grades 
# GROUP BY grades.subject_id, grades.student_id), grades 
# join students on grades.student_id=students.id 
# where grades.subject_id = %s 
# GROUP BY grades.subject_id, grades.student_id, students.fullname
def select_2():
    ...
# Знайти середній бал у групах з певного предмета.
def select_3():
    ...
# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    ...
# Знайти які курси читає певний викладач.
def select_5():
    ...
# Знайти список студентів у певній групі.
def select_6():
    ...
# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7():
    ...
# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8():
    ...
# Знайти список курсів, які відвідує певний студент.
def select_9():
    ...
# Список курсів, які певному студенту читає певний викладач.
def select_10():
    ...

print (select_1())