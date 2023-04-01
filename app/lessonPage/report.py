from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Record,Student,Teacher
from . import lessonPage

from app.auth import tokenUtils
from app.utils import fileHandle
import time 


@lessonPage.route('/report/list',methods = ['POST'])
@tokenUtils.token_required
def reportList(user_id,role):
	
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
			reportListDB = Record.query.filter_by(lesson_id = lesson_id).all();
			reportList = []
			index = 0 
			for report in reportListDB:
				aReport = {}
				index = index + 1
				aReport['index'] = index
				aReport['id'] = report.id
				student_id = report.student_id
				student = Student.query.filter_by(id = student_id).first()
				if student is not None:
					aReport['name'] = student.name
					aReport['account'] = student.account
				aReport['status'] = report.report_status
				aReport['report_url'] = report.report_url
				aReport['report_name'] = report.report_name
				reportList.append(aReport)
			data = {'reportList':reportList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

@lessonPage.route('/report/student',methods = ['POST'])
@tokenUtils.token_required
def studentReport(user_id,role):
	
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
			recordListDB = Record.query.filter_by(lesson_id = lesson_id,student_id=student.id).all();
			reportList = []
			index = 0 
			for record in recordListDB:
				aRecord = {}
				index = index + 1
				aRecord['name'] = record.report_name
				aRecord['id'] = record.id
				aRecord['content'] = record.content
				aRecord['status'] = record.report_status
				aRecord['file_name'] = record.report_file_name
				aRecord['report_url'] = record.report_url
				reportList.append(aRecord)
			data = {'reportList':reportList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)




@lessonPage.route('/report/detail',methods = ['POST'])
@tokenUtils.token_required
def reportDetail(user_id,role):

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
			record = Record.query.filter_by(id = id).first();
			result = {}
			if record is not None:
				result['report_name'] = record.report_name
				result['content'] = record.content
				result['report_status'] = record.report_status
				result['report_url'] = record.report_url
				result['report_file_name'] = record.report_file_name
				file_type = record.report_file_name.split('.')[1]
				result['file_type'] = file_type
				result['report_score'] = record.report_score
				result['report_feedback'] = record.report_feedback
			data = {'result':result}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

@lessonPage.route('/report/add',methods = ['POST'])
@tokenUtils.token_required
def addReport(user_id,role):
	
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
			title = values.get('title')
			content = values.get('content')

			record = Record.query.filter_by(lesson_id=lesson_id,student_id=student.id).first()
			if record is not None:
				record.content = content 
				record.report_name = title
				record.report_status = 1
				db.session.add(record)
				db.session.commit()

				data = {}
				code = 200
				msg = "add report success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)



@lessonPage.route('/report/addFile',methods = ['POST'])
@tokenUtils.token_required
def addReportFile(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.form
	lesson_id = values.get('lessonId')

	files = request.files
	file = files.get('file')

	if role == 'student' and lesson_id is not None and file is not None:
		student = Student.query.filter_by(id = user_id).first()
		if student is None:
			code = 201
			msg = "none student"
		else:
			result = fileHandle.upload(file)
			name = result.get('name')
			type = result.get('type')
			md5_str = result.get('md5_str')

			record = Record.query.filter_by(lesson_id=lesson_id,student_id=student.id).first()
			if record is not None:
				record.report_url = md5_str
				record.report_file_name = file.filename
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


@lessonPage.route('/report/score',methods = ['POST'])
@tokenUtils.token_required
def addReportScore(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	evaluate = values.get('evaluate')
	score = values.get('score')
	id = values.get('recordId')

	if role == 'teacher' and id is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:

			record = Record.query.filter_by(id=id).first()
			if record is not None:
				record.report_score = score
				record.report_feedback = evaluate
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


