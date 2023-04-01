from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Record,Student,Teacher
from . import lessonPage

from app.auth import tokenUtils
import time 

@lessonPage.route('/score/list',methods = ['POST'])
@tokenUtils.token_required
def scoreList(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	lesson_id = values.get('lessonId')

	if role == 'teacher' and lesson_id is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			recordListDB = Record.query.filter_by(lesson_id = lesson_id).all();
			scoreList = []
			index = 0
			for record in recordListDB:
				aRecord = {}
				index = index + 1
				aRecord['index'] = index
				aRecord['id'] = record.id
				student_id = record.student_id
				student = Student.query.filter_by(id = student_id).first()
				if student is not None:
					aRecord['name'] = student.name
					aRecord['account'] = student.account
				aRecord['arrivedTime'] = record.sign_time
				aRecord['lessonScore'] = record.lesson_score
				aRecord['reportScore'] = record.report_score
				aRecord['lessonScoreShow'] = True
				scoreList.append(aRecord)
			data = {'scoreList':scoreList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

@lessonPage.route('/score/student',methods = ['POST'])
@tokenUtils.token_required
def myScore(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	lesson_id = values.get('lessonId')

	if role == 'student' and lesson_id is not None:
		student = Student.query.filter_by(id = user_id).first()
		if student is None:
			code = 201
			msg = "none student"
		else:
			recordListDB = Record.query.filter_by(lesson_id = lesson_id,student_id= student.id).all();
			scoreList = []
			for record in recordListDB:
				aRecord = {}
				aRecord['id'] = record.id
				student_id = record.student_id
				student = Student.query.filter_by(id = student_id).first()
				if student is not None:
					aRecord['name'] = student.name
					aRecord['account'] = student.account
				aRecord['arrivedTime'] = record.sign_time
				aRecord['lessonScore'] = record.lesson_score
				aRecord['reportScore'] = record.report_score
				scoreList.append(aRecord)
			data = {'scoreList':scoreList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

@lessonPage.route('/score/edit',methods = ['POST'])
@tokenUtils.token_required
def scoreEdit(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	id = values.get('id')
	lesson_score = values.get('lessonScore')

	if role == 'teacher' and id is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			record = Record.query.filter_by(id = id).first();
			if record is not None:
				record.lesson_score = lesson_score
				db.session.add(record)
				db.session.commit()
				data = {}
				code = 200
				msg = "edit score success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)