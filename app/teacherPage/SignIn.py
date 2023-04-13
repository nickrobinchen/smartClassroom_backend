from flask import request
from flask import jsonify, Flask, current_app
from app import db
from app.models import Manager, Teacher, SignIn, SignInRecord, Student, Lecture, Class
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

        index = random.sample(students, int(stu_num / 1.5))
        print(index)
        for i in index:
            sim_signin = SignInRecord(signin_id=id,student_id=i,signin_time=int(time.time()*1000))
            print(sim_signin)
            db.session.add(sim_signin)
            db.session.commit()
            time.sleep(3)
            if SignIn.query.with_entities(SignIn.ended).filter_by(id=id).first()[0]:
                break

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
    start_time = values.get('start_time')

    signin = SignIn(lecture, end_time, start_time)
    db.session.add(signin)
    db.session.commit()
    signin_id = SignIn.query.with_entities(SignIn.id).filter_by(lecture_id=lecture,start_time=start_time).first()[0]

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
    signin = SignIn.query.filter_by(id=id).first()
    if signin.ended:
        result = getSigningResult(id)
    elif signin.end_time < int(time.time()*1000):
        result = getSigningResult(id)

        # 2:进行更新操作
        db.session.execute(db.update(SignIn).where(SignIn.id == id).values(ended=True))
        # 3：提交与关闭
        db.session.commit()
    else:
        signIns = SignInRecord.query.filter_by(signin_id=id).all()
        data = list(map(lambda r:{'name':Student.query.with_entities(Student.name).filter_by(id=r.student_id).first()[0],'id':r.student_id, 'signin_time':r.signin_time}, signIns))
        msg="Get Info Success"
        code = 200
        result={'ended': False, 'data': data}
    json_to_send = dict(code=code, message=msg, result=result)

    return jsonify(json_to_send)

def getSigningResult(id):
    sign_in = SignIn.query.filter_by(id=id).first()
    class_id = Lecture.query.with_entities(Lecture.class_id).filter_by(id=sign_in.lecture_id).first()[0]
    _class = Class.query.filter_by(id=class_id).first()
    students = Student.query.filter_by(class_id=_class.id).all()
    signIns = SignInRecord.query.filter_by(signin_id=id).all()
    stu_num = len(students)
    signed_num = len(signIns)
    signIn_ids = list(map(lambda i: i.student_id, signIns))
    unsigned_list = []
    for s in students:
        if s.id not in signIn_ids:
            unsigned_list.append(s.name)
    signed_students = list(map(lambda r:{'name':Student.query.with_entities(Student.name).filter_by(id=r.student_id).first()[0],'id':r.student_id, 'signin_time':r.signin_time}, signIns))
    return {'ended':True,'data':{'total_num':stu_num, 'signed_num': signed_num,'signed_students':signed_students,'unsigned_students':unsigned_list,'start_time':sign_in.start_time,'end_time':sign_in.end_time}}


@teacherPage.route('/signIn/end', methods=['GET'])
@tokenUtils.token_required
def endSigningIn(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    id = request.args.get('signin_id')
    signIn = SignIn.query.filter_by(id=id).first()
    signIn.ended = True
    code = 200
    msg = 'Signing Finished, returning results'
    json_to_send = {
        'code': code,
        'message': msg,
        'result': getSigningResult(id)
    }

    return jsonify(json_to_send)

@teacherPage.route('/signIn/prev', methods=['GET'])
@tokenUtils.token_required
def getPrevSignIns(user_id, role):
    code = 205
    msg = 'unknown error'
    data = {}
    lec_id = request.args.get('lec_id')
    signIns = SignIn.query.filter_by(lecture_id=lec_id).all()
    results = []
    for i in signIns:
        if not i.ended:
            if i.end_time < int(time.time()*1000):
                # 2:进行更新操作
                db.session.execute(db.update(SignIn).where(SignIn.id == i.id).values(ended=True))
                # 3：提交与关闭
                db.session.commit()
            else:
                continue
        results.append(getSigningResult(i.id)['data'])
    code = 200
    print(results)
    print(len(results))
    json_to_send = {
        'code': code,
        'message': msg,
        'result': results
    }

    return jsonify(json_to_send)


