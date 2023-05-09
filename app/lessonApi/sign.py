from flask import request
from flask import jsonify
from app import db
from app.models import Manager, Record, Teacher, Student, SignInRecord, Class, Lecture, SignIn, Course
from . import lessonPage

from app.auth import tokenUtils
import time


@lessonPage.route('/signIn/student', methods=['POST'])
@tokenUtils.token_required
def doSign(user_id, role):
    code = 205
    msg = 'unknown error'
    results = []
    data = {}

    values = request.json

    if role == 'student' and user_id is not None:
        code = 200
        msg = 'success'
        student = Student.query.filter_by(id=user_id).first()
        _class = Class.query.filter_by(id=student.class_id).first()
        lectures = Lecture.query.filter_by(class_id=student.class_id, status=1).all()
        if not len(lectures):
            data['type'] = 'warning'
            data['message'] = '无课程'
            data['description'] = '您当前无正在学习的课程！'
            results.append(data)
        else:
            data['type'] = 'warning'
            for lecture in lectures:
                signIns = SignIn.query.filter_by(lecture_id=lecture.id).all()
                for signIn in signIns:
                    if signIn.ended or signIn.end_time < time.time() * 1000:
                        continue
                    record = SignInRecord.query.filter_by(signin_id=signIn.id, student_id=student.id).first()
                    if record is not None:
                        data['type'] = 'warning'
                        data['message'] = '已签到'
                        data['description'] = '您已经签过到了！课程：' + \
                                              Course.query.with_entities(Course.name).filter_by(
                                                  id=Lecture.query.with_entities(Lecture.course_id).filter_by(
                                                      id=signIn.lecture_id).first()[
                                                      0])[0]
                        results.append(data)
                    else:
                        data['type'] = 'success'
                        data['message'] = '已签到'
                        data['description'] = '已完成签到！课程：' + Course.query.with_entities(Course.name).filter_by(
                            id=Lecture.query.with_entities(Lecture.course_id).filter_by(id=signIn.lecture_id).first()[
                                0]).first()[0]
                        record = SignInRecord(signin_id=signIn.id,student_id=student.id,signin_time=int(time.time()* 1000))
                        db.session.add(record)
                        db.session.commit()
                        results.append(data)
                if not len(results):
                    data['type'] = 'warning'
                    data['message'] = '无签到'
                    data['description'] = '您的课程中没有开启的签到！'
                    results.append(data)

    json_to_send = {
        'code': code,
        'msg': msg,
        'result': results
    }

    return jsonify(json_to_send)


@lessonPage.route('/signIn/list', methods=['POST'])
@tokenUtils.token_required
def signInList(user_id, role):
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
            lesson_id = values.get('lessonId')

            if lesson_id is not None:
                recordListDB = Record.query.filter_by(lesson_id=lesson_id).all();
                signInList = []
                for record in recordListDB:
                    aRecord = {}
                    aRecord['id'] = record.id
                    student_id = record.student_id
                    student = Student.query.filter_by(id=student_id).first()
                    if student is not None:
                        aRecord['name'] = student.name
                        aRecord['account'] = student.account
                    aRecord['arrivedTime'] = record.sign_time
                    aRecord['status'] = record.sign_status
                    signInList.append(aRecord)
                data = {'signInList': signInList}
                code = 200
                msg = "success"

    json_to_send = {
        'code': code,
        'msg': msg,
        'data': data
    }

    return jsonify(json_to_send)
