from flask import request
from flask import jsonify
from app import db
from app.models import Course, Manager, Teacher, Lecture, Class, Lesson, Record, Student
from . import coursePage

from app.auth import tokenUtils
import time, datetime


@coursePage.route('/course/add', methods=['POST'])
@tokenUtils.token_required
def add(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}

    if role == 'manager' or role == 'admin':
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
        'result': data
    }
    print(json_to_send)
    return jsonify(json_to_send)


@coursePage.route('/lecture/add', methods=['POST'])
@tokenUtils.token_required
# todo: 恢复这里的权限处理
def addcourseforteacher(user_id, role):
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
            print(values)
            class_id = values.get('class')
            course_id = values.get('course')
            weekDate = values.get('weekDate')
            startAndEndDate = values.get('startAndEndDate')

            if class_id is None or course_id is None or weekDate is None \
                    or startAndEndDate is None:

                code = 202

                msg = 'parameter error'
            else:
                try:

                    start_date = startAndEndDate[0]
                    end_date = startAndEndDate[1]

                    week_date = "、".join(weekDate)

                    status = 1
                    courseforteacher = Lecture(course_id, teacher_id, class_id, start_date, end_date,
                                               week_date, status)
                    print(courseforteacher)
                    if Lecture.query.filter_by(course_id=course_id, teacher_id=teacher_id, class_id=class_id).first() is not None:
                        msg = 'Lecture already exists!'
                    else:
                        db.session.add(courseforteacher)
                        db.session.commit()

                        if courseforteacher.id is not None:
                            students = Student.query.with_entities(Student.id).filter_by(class_id=class_id).all()
                            lessons = []
                            for s in students:
                                db.session.add(Lesson(lecture_id=courseforteacher.id,student_id=s[0]))
                            db.session.commit()
                            # todo: What is this?
                            # addLessons(courseforteacher.id, start_date, end_date, weekDate, klass_id)
                        data = {"id": courseforteacher.id}
                        code = 200
                        msg = 'add course for teacher success'
                except Exception as e:
                    print(e)
                    pass
    else:
        code = 201
        msg = 'access deny'

    json_to_send = {
        'code': code,
        'msg': msg,
        'result': data
    }
    print(json_to_send)
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
