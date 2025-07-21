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
def select_6(group):
    stmt = select(
            Student.fullname
        ).join(
            Groups
        ).where(
            Groups.name==group
        )
    result = session.execute(stmt).mappings().all()
    return result
# Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group, subject):
    stmt = select(
            Student.fullname,
            func.array_agg(Grades.grade).label('grades_list')
        ).select_from(
            Student
        ).join(
            Groups
        ).join(
            Grades
        ).join(
            Subjects
        ).where(
            Groups.name==group,
            Subjects.name==subject
        ).group_by(
            Student.fullname
        )
    result = session.execute(stmt).mappings().all()
    return result
# Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8():
    stmt = select(
            Teachers.fullname,
            func.round(
                func.avg(Grades.grade), 3
            ).label('avg_grade')
        ).select_from(
            Teachers
        ).join(
            Subjects
        ).join(
            Grades
        ).group_by(
            Teachers.fullname
        )
    result = session.execute(stmt).mappings().all()
    return result
# Знайти список курсів, які відвідує певний студент.
def select_9(student):
    stmt = select(
            Student.fullname,
            func.array_agg(
                func.distinct(Subjects.name)
            ).label('subject_list'),
        ).select_from(
            Student
        ).join(
            Grades
        ).join(
            Subjects
        ).where(Student.fullname==student
        ).group_by(
            Student.fullname
        )
    result = session.execute(stmt).all()
    return result
# Список курсів, які певному студенту читає певний викладач.
def select_10(student, teacher):
    stmt = select(
            Student.fullname,
            func.array_agg(
                func.distinct(Subjects.name)
            ).label('subject_list'),
        ).select_from(
            Student
        ).join(
            Grades
        ).join(
            Subjects
        ).join(
            Teachers
        ).where(
            Student.fullname==student,
            Teachers.fullname==teacher   
        ).group_by(
            Student.fullname
        )
    result = session.execute(stmt).all()
    return result

if __name__ == '__main__':


    print(">>>>> select_1") 
    i=1
    for row in select_1():
        print(f"{i}) {row.fullname}, з середнім балом {row.avg_grade}")
        i+=1

    print(">>>>> select_2") 
    for name, fullname, avg_grade in select_2(5):
        print(f'На предметі "{name}" кращий студент\n {fullname}, з середнім балом {avg_grade}')
    
    print(">>>>> select_3") 
    print(f'Предмет \t\t\t Група \t\t Середній бал')
    for row in select_3('Системне програмування'):
        print(f'"{row.name_1}" \t  {row.name} \t {row.avg_grade}')
    
    print(">>>>> select_4") 
    for row in select_4():
        print(f'"{row.name}" середній бал - {row.round}')

    print(">>>>> select_5") 
    teacher_name = "добродій Семен Кабаненко"
    print(f"{teacher_name} викладає:")
    i=1
    for subject in select_5(teacher_name):
        print(f'{i}) {subject.name};')
        i+=1
    

    print(">>>>> select_6")  
    i=1
    group='ФІОТ-25'
    print(f'Група {group}:')
    for subject in select_6(group):
        print(f'{i}) {subject.fullname};')
        i+=1

    i=1
    group='ФІОТ-25'
    subject='Мережі та телекомунікації'
    print(">>>>> select_7")    
    print(f'Оцінки групи {group} за предметом {subject}:')
    for student in select_7(group, subject):
         print(f'{i}) {student.fullname} - {student.grades_list};')
         i+=1

    i=1
    print(">>>>> select_8")
    for teacher in select_8():
         print(f'{i}) {teacher.fullname} - {teacher.avg_grade};')
         i+=1

    print(">>>>> select_9")
    i=1
    student="Усик Опанас Лукʼянович"
    for fullname, subject_list in select_9(student):
        print(f"Студент {fullname} відвідує наступні курси:")
        for ithem in subject_list:
            print(f"{i}) {ithem}")
            i+=1

    print(">>>>> select_10")
    i=1
    student="Усик Опанас Лукʼянович"
    teacher="Орхип Радченко"
    for fullname, subject_list in select_10(student, teacher):
        print(f"Студент {fullname} відвідує наступні курси викладача {teacher}:")
        for ithem in subject_list:
            print(f"{i}) {ithem}")
            i+=1