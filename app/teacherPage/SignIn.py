from flask import request
from flask import jsonify, Flask, current_app
from app import db
from app.models import Manager, Teacher, SignIn, SignInRecord,Student, Lecture
from . import teacherPage
import asyncio
from app.auth import tokenUtils
import random, threading, time

def simulate_signin(app, id, lec_id):
    with app.app_context():
        class_id = Lecture.query.with_entities(Lecture.class_id).filter_by(id=lec_id).first()[0]
        print(class_id)

        students_1 = Lecture.query.with_entities(Student.id).filter_by(class_id=class_id).all()
        students = list(map(lambda i: i[0], students_1))
        print(students)
        stu_num = len(students)

        index = random.sample(students, int(stu_num / 2))
        print(index)
        for i in index:
            sim_signin = SignInRecord(signin_id=id,student_id=i,signin_time=int(time.time()*1000))
            print(sim_signin)
            db.session.add(sim_signin)
            db.session.commit()
            time.sleep(3)

@teacherPage.route('/signIn/add', methods=['POST'])
@tokenUtils.token_required
def beginSigningIn(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}

    values = request.json
    print(values)
    lecture = values.get('lec_id')
    end_time = values.get('end_time')

    signin = SignIn(lecture, end_time)
    db.session.add(signin)
    db.session.commit()
    signin_id = SignIn.query.with_entities(SignIn.id).filter_by(lecture_id=lecture,end_time=end_time).first()[0]

    t = threading.Thread(target=simulate_signin, args=(current_app._get_current_object(),signin_id,lecture),name='sim')
    t.start()
    print(data)
    code = 200
    json_to_send = {
        'code': code,
        'message': msg,
        'result': signin_id
    }

    return jsonify(json_to_send)

@teacherPage.route('/signIn/getInfo', methods=['GET'])
@tokenUtils.token_required
def getSigningInfo(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    id = request.args.get('id')
    signIns = SignInRecord.query.filter_by(signin_id=id).all()
    data = list(map(lambda r:{'name':Student.query.with_entities(Student.name).filter_by(id=r.student_id).first()[0],'id':r.student_id, 'signin_time':r.signin_time}, signIns))

    code = 200
    json_to_send = {
        'code': code,
        'message': msg,
        'result': data
    }

    return jsonify(json_to_send)


