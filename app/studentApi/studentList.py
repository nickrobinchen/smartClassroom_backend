from flask import request
from flask import jsonify
from app import db
from app.models import Student, Manager, Class, Teacher, Grade, Lesson, Course, Lecture
from . import studentPage

from app.auth import tokenUtils
import time


@studentPage.route('/student/list', methods=['POST'])
@tokenUtils.token_required
def studentList(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    if role == 'manager' or role == 'teacher' or role == 'super':

        values = request.json
        print(values)
        if values != {}:
            college = values.get("college")
            id = values.get("class_id")
            name = values.get("class")
            if id is not None:
                klass = Class.query.filter_by(id=id).first()
            else:
                klass = Class.query.filter_by(name=name).first()
            if klass is not None:
                id = klass.id
                studentListDB = Student.query.filter_by(class_id=id).all();
                studentList = []
                index = 0
                for student in studentListDB:
                    aStudent = {}
                    index = index + 1
                    aStudent['index'] = index
                    aStudent['id'] = student.id
                    aStudent['name'] = student.name
                    aStudent['account'] = student.account
                    aStudent['klass_id'] = student.class_id
                    aStudent['class'] = klass.name
                    aStudent['email'] = student.email
                    aStudent['tel'] = student.tel

                    studentList.append(aStudent)
                data = studentList  # {'studentList':studentList}
                code = 200
                msg = "success"

        else:
            studentListDB = Student.query.all();
            studentList = []
            index = 0
            for student in studentListDB:
                if student.class_id is None:
                    continue
                aStudent = {}
                index = index + 1
                aStudent['index'] = index
                aStudent['id'] = student.id
                aStudent['name'] = student.name
                aStudent['account'] = student.account
                aStudent['klass_id'] = student.class_id
                aStudent['class'] = Class.query.with_entities(Class.name).filter_by(id=student.class_id).first()[0]
                aStudent['email'] = student.email
                aStudent['tel'] = student.tel

                studentList.append(aStudent)
            data = studentList  # {'studentList':studentList}
            code = 200
            msg = "success"

    else:
        code = 202
        msg = 'access deny!'
    json_to_send = {
        'code': code,
        'msg': msg,
        'result': data
    }
    return jsonify(json_to_send)


@studentPage.route('/student/fullInfo', methods=['GET'])
@tokenUtils.token_required
def getFullInfo(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    student = Student.query.filter_by(id=user_id).first()
    if student is not None:
        data['name'] = student.name
        code = 200
        msg = "Get student name success, but student is in no class!"
        if student.class_id is not None:
            _class = Class.query.filter_by(id=student.class_id).first()
            data['classInfo'] = dict(id=student.class_id, class_name=_class.name,
                                     grade=Grade.query.with_entities(Grade.grade_name).filter_by(
                                         id=_class.belonged_grade).first()[0],
                                     college=_class.belonged_college)
            lessons = Lesson.query.filter_by(student_id=student.id).all()
            data['lessonInfo'] = []
            for l in lessons:
                lesson_info = dict(lesson_id=l.id,
                                   course_name=Course.query.with_entities(Course.name).filter_by(id=(
                                       Lecture.query.with_entities(Lecture.course_id).filter_by(
                                           id=l.lecture_id).first()[0])).first()[0],
                                   score=l.score)
                lecture = Lecture.query.filter_by(id=l.lecture_id).first()
                teacher_name = Teacher.query.with_entities(Teacher.name).filter_by(id=lecture.teacher_id).first()[0]

                weekDay = lecture.week_date.split("、")
                week = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

                # aCourse['weekday_array'] = list(map(lambda i: int(i) % 7, course.week_date.split("、")))
                lesson_info.update(dict(detail=dict(teacher_name=teacher_name,
                                                    start_date=lecture.start_date.strftime(
                                                        '%Y-%m-%d'),
                                                    end_date=lecture.end_date.strftime(
                                                        '%Y-%m-%d'),
                                                    weekday_array=list(
                                                        map(lambda i: int(i) % 7, lecture.week_date.split("、"))),
                                                    weekDay='、'.join(list(
                                                        map(lambda i: week[int(i) - 1],
                                                            weekDay))))))
                data['lessonInfo'].append(lesson_info)
                print(data)
                code = 200
                msg = "Get student's class and lesson info success!"

        print(data)
        json_to_send = {
            'code': code,
            'msg': msg,
            'result': data
        }
        return jsonify(json_to_send)
