from db_connection import session
from sqlalchemy import func, desc, select
from models import Teachers, Groups, Student, Subjects, Grades

# Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    stmt = select(
        Student.fullname, 
        func.round(func.avg(Grades.grade), 2).label('avg_grade')
        ).select_from(
            Grades
            ).join(
                Student
                ).group_by(
                    Student.id
                    ).order_by(desc('avg_grade')
                               ).limit(5)
    result = session.execute(stmt).mappings().all()
    return result

# Знайти студента із найвищим середнім балом з певного предмета.
def select_2(id_of_subject):
    stmt = select(
        Subjects.name, 
        Student.fullname, 
        func.round(func.avg(Grades.grade), 2).label('avg_grade')
        ).select_from(
            Grades
            ).join(
                Subjects
                   ).join(
                       Student
                          ).where(
                              Grades.subject_id==id_of_subject
                                  ).group_by(
                                      Subjects.name,Student.id
                                             ).order_by(desc('avg_grade')
                                                        ).limit(1)
    result = session.execute(stmt).all()
    return result

# Знайти середній бал у групах з певного предмета.
def select_3(subject_name):
    stmt = select(
        func.round(
            func.avg(Grades.grade), 2
            ).label('avg_grade'), 
            Groups.name, 
            Subjects.name
            ).select_from(
                Grades
                ).join(
                    Student
                    ).join(
                        Groups
                        ).join(
                            Subjects
                            ).where(
                                Subjects.name == subject_name
                                ).group_by(
                                Groups.name, 
                                Grades.subject_id, 
                                Subjects.name
                                )
    result = session.execute(stmt).mappings().all()
    return result

# Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    stmt = select(
        Groups.name,
        func.round(
            func.avg(Grades.grade), 3)
            ).select_from(
                Grades
                ).join(
                    Student
                    ).join(
                        Groups
                        ).group_by(
                            Student.group_id, 
                            Groups.name
                            )
    result = session.execute(stmt).mappings().all()
    return result

# Знайти які курси читає певний викладач.
# SELECT subjects.name 
# from teachers 
# join subjects on teachers.id = subjects.teacher_id 
# where teachers.fullname = %s
def select_5(teacher):
    stmt = select(
        Subjects.name
    ).select_from(
        Teachers
    ).join(
        Subjects, 
        Teachers.id == Subjects.teacher_id
    ).where(
        Teachers.fullname == teacher
    )
    result = session.execute(stmt).mappings().all()
    return result
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

if __name__ == '__main__':

    i=1
    for row in select_1():
        print(f"{i}) {row.fullname}, з середнім балом {row.avg_grade}")
        i+=1

    for name, fullname, avg_grade in select_2(5):
        print(f'На предметі "{name}" кращий студент\n {fullname}, з середнім балом {avg_grade}')
    
    print(f'Предмет \t\t\t Група \t\t Середній бал')
    for row in select_3('Системне програмування'):
        print(f'"{row.name_1}" \t  {row.name} \t {row.avg_grade}')
    
    for row in select_4():
        print(f'"{row.name}" середній бал - {row.round}')

    teacher_name = "добродій Семен Кабаненко"
    print(f"{teacher_name} викладає:")
    i=1
    for subject in select_5(teacher_name):
        print(f'{i}) {subject.name};')
        i+=1
    