from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Student,Class,Teacher
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/add',methods = ['POST'])
@tokenUtils.token_required
def addStudent(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager' or role == 'teacher':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			values = request.json
			name = values.get('name')
			account = values.get('account')
			tel = values.get('tel')
			email = values.get('email')
			# college = values.get('college')
			# grade = values.get('grade')
			# klass_name = values.get('klass')
			class_id = values.get('student_class')
			if name is None or account is None:
				code = 202
				msg = 'parameter error'
			else:
				try:
					# klass = Class.query.filter_by(n).first()
					# if klass is not None:
					# 	klass_id = klass.id
					password = 'student'#account[-6:]
					student = Student(name,account,tel,class_id,email,password)
					db.session.add(student)
					db.session.commit()

					code = 200
					msg = 'success'
				except:
					pass
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)



@studentPage.route('/student/addCollege',methods = ['POST'])
@tokenUtils.token_required
def addCollege(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager' or role == 'teacher':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			values = request.json
			college_name = values.get('name')

			if college_name is None:
				code = 202
				msg = 'parameter error'
			else:
				klass = Klass.query.filter_by(belonged_college=college_name).first()
				if klass is None:
					aKlass = Klass("","",college_name)
					db.session.add(aKlass) 
					db.session.commit()

				code = 200
				msg = 'success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)


@studentPage.route('/student/addKlass',methods = ['POST'])
@tokenUtils.token_required
def addKlass(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager' or role == 'teacher':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			values = request.json
			name = values.get('name')
			grade = values.get('grade')
			college = values.get('college')			

			if name is None or grade is None or college is None:
				code = 202
				msg = 'parameter error'
			else:
				klass = Klass.query.filter_by(name=name,belonged_grade=grade,belonged_college=college).first()
				if klass is None:
					aKlass = Klass(name,grade,college)
					db.session.add(aKlass) 
					db.session.commit()

				code = 200
				msg = 'success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

