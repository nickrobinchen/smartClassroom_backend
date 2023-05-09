from flask import request
from flask import jsonify
from sqlalchemy import func

from app import db
from app.models import Manager, Teacher, Student, Class, Lecture, Course
from . import managerPage

from app.auth import tokenUtils
import time


def getRelation():
    result = {'nodes': [], 'links': []}
    teachers = db.session.query(Teacher.id, Teacher.name).all()
    classes = db.session.query(Class.id, Class.name).all()
    courses = db.session.query(Course.id, Course.name).all()
    lectures = db.session.query(Lecture.id, Lecture.class_id, Lecture.teacher_id, Lecture.course_id).all()
    t_len = len(teachers)
    i = 1
    for t_id, t_name in teachers:
        result['nodes'].append({'name': t_name, 'id': 'teacher_' + str(t_id), 'x': (i * 500 / t_len) + 50, 'y': 50})
        i = i + 1
    i = 1
    c_len = len(classes)
    for c_id, c_name in classes:
        result['nodes'].append({'name': c_name, 'id': 'class_' + str(c_id), 'x': (i * 500 / c_len) + 50, 'y': 200})
        i = i + 1
    # for cour_id, cour_name in courses:
    #     result['nodes'].append({'name': cour_name, 'id': 'course_' + str(cour_id)})
    for lec_id, class_id, t_id, cour_id in lectures:
        for _id, cour_name in courses:
            if _id == cour_id:
                result['links'].append(
                    {'source': 'teacher_' + str(t_id), 'target': 'class_' + str(class_id), 'relation': {
                        'name': "教授课程:" + cour_name
                    }, })
    return result


@managerPage.route('/manager/basicData', methods=['GET'])
@tokenUtils.token_required
def getManagerInfo(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    if role == 'manager' or role == 'admin':
        student_class_data = db.session.query(Student.class_id, func.count('*')).group_by(Student.class_id).all()
        studen_sum = Student.query.count()
        class_info = db.session.query(Class.id, Class.name).all()
        data['student'] = {'total': studen_sum, 'classes': []}
        for class_id, count in student_class_data:
            if class_id is None:
                data['student']['classes'].append(dict(id=-1, name='其他', count=count))
            for _id, name in class_info:
                if _id == class_id:
                    data['student']['classes'].append(dict(id=class_id, name=name, count=count))
        data['teacher_class_relation'] = getRelation()
        code = 200
        msg = 'success'
    json_to_send = {
        'code': code,
        'msg': msg,
        'result': data
    }
    return jsonify(json_to_send)
