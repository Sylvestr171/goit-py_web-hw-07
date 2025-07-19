from sqlalchemy import String, ForeignKey, Date, inspect
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from datetime import date

Base = declarative_base()

class Base_tamplate(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)

class Teachers(Base_tamplate):
    __tablename__ = 'teachers'
    fullname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120))

class Groups(Base_tamplate):
    __tablename__ = 'groups'
    name: Mapped[str] = mapped_column(String(20), nullable=False)

class Student(Base_tamplate):
    __tablename__ = 'students'
    fullname: Mapped[str] = mapped_column(String(120), nullable=False)
    group_id: Mapped[int] = mapped_column('group_id', ForeignKey('groups.id', ondelete='CASCADE'))
    group: Mapped[Groups] = relationship('Groups', backref='students')

class Subjects(Base_tamplate):
    __tablename__ = 'subjects'
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    teacher_id: Mapped[int] = mapped_column('teacher_id', ForeignKey('teachers.id', ondelete='CASCADE'))
    teacher: Mapped[Teachers] = relationship('Teachers', backref='disciplines')

class Grades(Base_tamplate):
    __tablename__ = 'grades'
    grade: Mapped[int] = mapped_column(nullable=False)
    grade_date: Mapped[date] = mapped_column('grade_date', Date, nullable=True)
    student_id: Mapped[int] = mapped_column('student_id', ForeignKey('students.id', ondelete='CASCADE'))
    subject_id: Mapped[int] = mapped_column('subject_id', ForeignKey('subjects.id', ondelete='CASCADE'))
    student: Mapped[Student] = relationship('Student', backref='grade')
    discipline: Mapped[Subjects] = relationship('Subjects', backref='grade')

# if __name__ == '__main__':
#     from sqlalchemy import inspect
#     from db_connection import engine
#     inspector = inspect(engine)
#     tables = inspector.get_table_names()

#     print("Таблиці в базі:", tables)