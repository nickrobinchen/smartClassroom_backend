from app import db
from sqlalchemy import ForeignKey

class Grade(db.Model):

    # 定义表名
    __tablename__ = 'grade'

    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True, nullable = False)
    grade_name = db.Column(db.String(45), nullable = True)
    grade_ref = db.Column(db.String(45), nullable = True)

    def __init__(self, grade_name, grade_ref):
        self.grade_name = grade_name
        self.grade_ref = grade_ref

    def __repr__(self):
        return self.grade_ref + self.grade_name
class Manager(db.Model):

    # 定义表名
    __tablename__ = 'manager'

    id = db.Column(db.INTEGER, primary_key = True, autoincrement = True, nullable = False)
    account = db.Column(db.String(45), nullable = True)
    password = db.Column(db.String(45), nullable = False)

    def __init__(self, account, password):
        self.account = account
        self.password = password

    def __repr__(self):
        return '<Manager {}>'.format(self.account)

class Teacher(db.Model):

    # 定义表名
    __tablename__ = 'teacher'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    account = db.Column(db.String(45))
    tel = db.Column(db.String(45))
    address = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))

    def __init__(self, name, account,tel,address,email,password):
        self.name = name
        self.account = account
        self.tel = tel
        self.address = address
        self.email = email
        self.password = password


    def __repr__(self):
        return '<teacher {}>'.format(self.name)

class Student(db.Model):

    # 定义表名
    __tablename__ = 'student'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    account = db.Column(db.String(45))
    tel = db.Column(db.String(45))
    email = db.Column(db.String(45))
    class_id = db.Column(db.INTEGER)
    password = db.Column(db.String(45))


    def __init__(self, name, account, tel, class_id, email, password):
        self.name = name
        self.account = account
        self.tel = tel
        self.class_id = class_id
        self.email = email
        self.password = password

    def __repr__(self):
        return '<student {}>'.format(self.name)

class Course(db.Model):

    # 定义表名
    __tablename__ = 'course'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    grade = db.Column(db.String(45))

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __repr__(self):
        return '<Course {}>'.format(self.name)

class SignInRecord(db.Model):

    # 定义表名
    __tablename__ = 'signin_records'

    id = db.Column(db.INTEGER, primary_key=True)
    signin_id = db.Column(db.INTEGER)
    student_id = db.Column(db.INTEGER)
    signin_time = db.Column(db.BIGINT)
    extra_info = db.Column(db.INTEGER)

    def __init__(self, signin_id, student_id, signin_time,extra_info=0):
        self.signin_id = signin_id
        self.student_id = student_id
        self.signin_time = signin_time
        if extra_info:
            self.extra_info = extra_info
class SignIn(db.Model):

    # 定义表名
    __tablename__ = 'signin'

    id = db.Column(db.INTEGER, primary_key=True)
    lecture_id = db.Column(db.INTEGER)
    end_time = db.Column(db.BIGINT)
    start_time = db.Column(db.BIGINT)
    ended = db.Column(db.BOOLEAN)

    def __init__(self, lec_id, end_time, start_time):
        self.lecture_id = lec_id
        self.end_time = end_time
        self.start_time = start_time
        self.ended = False
class Lecture(db.Model):

    # 定义表名
    __tablename__ = 'lecture'

    id = db.Column(db.INTEGER, primary_key=True)
    course_id = db.Column(db.INTEGER)
    teacher_id = db.Column(db.INTEGER)
    class_id = db.Column(db.INTEGER)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    week_date = db.Column(db.String(45))
    status = db.Column(db.INTEGER)

    def __init__(self, course_id, teacher_id,class_id,start_date,end_date,week_date,status):

        self.course_id = course_id
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.start_date = start_date
        self.end_date = end_date
        self.week_date = week_date
        self.status = status


    def __repr__(self):
        return '<CourseForTeacher {}>'.format(self.id)

# class Lesson(db.Model):
#
#     # 定义表名
#     __tablename__ = 'lesson'
#
#     id = db.Column(db.INTEGER, primary_key=True)
#     courseforteacher_id = db.Column(db.INTEGER)
#     date = db.Column(db.Date)
#     week_date = db.Column(db.String(45))
#
#     def __init__(self,courseforteacher_id,date,week_date):
#         self.courseforteacher_id = courseforteacher_id
#         self.date = date
#         self.week_date = week_date
#
#     def __repr__(self):
#         return '<student {}>'.format(self.id)

class Class(db.Model):

    # 定义表名
    __tablename__ = 'class'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))
    belonged_grade = db.Column(db.String(45))
    belonged_college = db.Column(db.String(45))

    def __init__(self,name,belonged_grade,belonged_college):
        self.name = name
        self.belonged_grade = belonged_grade
        self.belonged_college = belonged_college

    def __repr__(self):
        return '<class {}>'.format(self.name)

class College(db.Model):

    # 定义表名
    __tablename__ = 'college'

    id = db.Column(db.INTEGER, primary_key=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<student {}>'.format(self.id)

class Record(db.Model):

    # 定义表名
    __tablename__ = 'record'

    id = db.Column(db.INTEGER, primary_key=True)
    lesson_id = db.Column(db.INTEGER)
    student_id = db.Column(db.INTEGER)
    report_status = db.Column(db.INTEGER)
    sign_status = db.Column(db.INTEGER)
    report_url = db.Column(db.String(45))
    content = db.Column(db.String(225))
    sign_time = db.Column(db.String(45))
    lesson_score = db.Column(db.String(45))
    report_score = db.Column(db.String(45))
    report_feedback = db.Column(db.String(45))
    report_name = db.Column(db.String(45))
    report_file_name = db.Column(db.String(45))
    


    def __init__(self,lesson_id,student_id,report_status,sign_status,report_url,content,sign_time,lesson_score,report_score):
        self.lesson_id = lesson_id
        self.student_id = student_id
        self.report_status = report_status
        self.sign_status = sign_status
        self.report_url = report_url
        self.content = content
        self.sign_time = sign_time
        self.lesson_score = lesson_score
        self.report_score = report_score

    def __repr__(self):
        return '<record {}>'.format(self.id)

class Message(db.Model):

    # 定义表名
    __tablename__ = 'message'

    id = db.Column(db.INTEGER, primary_key=True)

    def __init__(self):
        pass

    def __repr__(self):
        return '<student {}>'.format(self.id)

class Lab(db.Model):

    # 定义表名
    __tablename__ = 'lab'

    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(45))


    def __init__(self,name):
        self.name = name

    def __repr__(self):
        return '<student {}>'.format(self.id)

class Note(db.Model):

    # 定义表名
    __tablename__ = 'note'

    id = db.Column(db.INTEGER, primary_key=True)
    lesson_id = db.Column(db.INTEGER)
    name = db.Column(db.String(45))
    type  = db.Column(db.String(45))
    md5_str = db.Column(db.String(45))

    def __init__(self,lesson_id,name,type,md5_str):

        self.lesson_id = lesson_id
        self.name = name
        self.type = type
        self.md5_str = md5_str

    def __repr__(self):
        return '<note {}>'.format(self.name)



class Lesson(db.Model):

    # 定义表名
    __tablename__ = 'lesson'

    id = db.Column(db.INTEGER, primary_key=True)
    lecture_id = db.Column(db.INT)
    student_id = db.Column(db.INT)
    score = db.Column(db.INT)

    def __init__(self,lecture_id,student_id):

        self.lecture_id = lecture_id
        self.student_id = student_id

    def __repr__(self):
        return '<lesson {}>'.format(self.id)