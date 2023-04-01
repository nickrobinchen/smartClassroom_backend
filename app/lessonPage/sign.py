from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Record,Teacher,Student
from . import lessonPage

from app.auth import tokenUtils
import time 

@lessonPage.route('/signIn/doSign',methods = ['POST'])
@tokenUtils.token_required
def doSign(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	id = values.get('recordId')

	if role == 'teacher' and id is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			record = Record.query.filter_by(id = id).first()
			if record is not None:
				record.sign_status = 1
				record.sign_time = time.strftime("%H:%M",time.localtime())
				
				db.session.add(record)
				db.session.commit()
			data = {}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)


@lessonPage.route('/signIn/list',methods = ['POST'])
@tokenUtils.token_required
def signInList(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'teacher':
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			values = request.json
			lesson_id = values.get('lessonId')
			
			if lesson_id is not None:
				recordListDB = Record.query.filter_by(lesson_id = lesson_id).all();
				signInList = []
				for record in recordListDB:
					aRecord = {}
					aRecord['id'] = record.id
					student_id = record.student_id
					student = Student.query.filter_by(id = student_id).first()
					if student is not None:
						aRecord['name'] = student.name
						aRecord['account'] = student.account
					aRecord['arrivedTime'] = record.sign_time
					aRecord['status'] = record.sign_status
					signInList.append(aRecord)
				data = {'signInList':signInList}
				code = 200
				msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

