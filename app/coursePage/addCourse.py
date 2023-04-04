from flask import request
from flask import jsonify
from app import db
from app.models import Course, Manager, Teacher, CourseForTeacher, Class, Lesson, Record, Student
from . import coursePage

from app.auth import tokenUtils
import time, datetime


@coursePage.route('/course/add', methods=['POST'])
@tokenUtils.token_required
def add(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}

    if role == 'manager':
        manager = Manager.query.filter_by(id=user_id).first()
        if manager is None:
            code = 201
            msg = "none manager"
        else:
            values = request.json
            name = values.get('name')
            grade = values.get('grade')
            if name is None or grade is None:
                code = 202
                msg = 'parameter error'
            else:
                course = Course(name, grade)
                db.session.add(course)
                db.session.commit()

                code = 200
                msg = 'success'

    else:
        code = 201
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    return jsonify(json_to_send)


@coursePage.route('/lecture/add', methods=['POST'])
@tokenUtils.token_required
def addcourseforteacher(yuser_id, yrole):
    role = 'teacher'
    user_id = 1
    teacher_id = user_id
    code = 205
    msg = 'unknown error'
    data = {}

    if role == 'teacher':
        teacher = Teacher.query.filter_by(id=user_id).first()
        if teacher is None:
            code = 201
            msg = "none teacher"
        else:
            values = request.json
            klass_info = values.get('class')
            course_id = values.get('course')
            weekDate = values.get('weekDate')
            startAndEndDate = values.get('startAndEndDate')

            if klass_info is None or course_id is None or weekDate is None \
                    or startAndEndDate is None:

                code = 202
                msg = 'parameter error'
            else:
                try:
                    college = klass_info[0]
                    grade = klass_info[1]
                    name = klass_info[2]

                    aKlass = Class.query.filter_by(belonged_college=college, belonged_grade=grade, name=name).first()
                    klass_id = aKlass.id

                    start_date = startAndEndDate[0]
                    end_date = startAndEndDate[1]

                    week_date = "、".join(weekDate)

                    status = 1
                    courseforteacher = CourseForTeacher(course_id, teacher_id, klass_id, start_date, end_date,
                                                        week_date, status)
                    db.session.add(courseforteacher)
                    db.session.commit()
                    if courseforteacher.id is not None:
                        addLessons(courseforteacher.id, start_date, end_date, weekDate, klass_id)
                    data = {"id": courseforteacher.id}
                    code = 200
                    msg = 'add course for teacher success'
                except:
                    pass
    else:
        code = 201
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    return jsonify(json_to_send)


def addLessons(courseforteacher_id, start_date_str, end_date_str, week_date, klass_id):
    week_arr = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    week_date_code_arr = []
    for date in week_date:
        index = week_arr.index(date) + 1
        week_date_code_arr.append(index)

    start_date = datetime.date.fromisoformat(start_date_str)
    end_date = datetime.date.fromisoformat(end_date_str)

    current_date = start_date

    while (current_date < end_date + datetime.timedelta(days=1)):
        week_date_code = current_date.isoweekday()
        if week_date_code in week_date_code_arr:

            week_date_str = week_arr[week_date_code - 1]
            lesson = Lesson(courseforteacher_id, current_date, week_date_str)
            db.session.add(lesson)
            db.session.commit()
            if lesson.id is not None:
                addRecords(lesson.id, klass_id)
        current_date = current_date + datetime.timedelta(days=1)
    db.session.commit()


def addRecords(lesson_id, klass_id):
    students = Student.query.filter_by(klass_id=klass_id).all()
    for student in students:
        record = Record(lesson_id, student.id, 0, 0, None, None, None, None, None)
        db.session.add(record)
