from flask import request
from flask import jsonify
from app import db
from app.models import Student,Manager,Klass,Teacher
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/list',methods = ['POST'])
@tokenUtils.token_required
def studentList(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}
	print((role,user_id))
	if role == 'manager' or role == 'teacher':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			values = request.json
			college = values.get("college")
			grade = values.get("grade")
			klass = values.get("klass")

			klass = Klass.query.filter_by(belonged_college=college,belonged_grade=grade,name=klass).first()
			if klass is not None:
				klass_id = klass.id			
				studentListDB = Student.query.filter_by(klass_id=klass_id).all();
				studentList = []
				index = 0
				for student in studentListDB:
					aStudent = {}
					index = index + 1
					aStudent['index'] = index
					aStudent['id'] = student.id
					aStudent['name'] = student.name
					aStudent['account'] = student.account
					aStudent['klass_id'] = student.klass_id
					aStudent['email'] = student.email
					aStudent['tel'] = student.tel

					studentList.append(aStudent)
				data = {'studentList':studentList}
				code = 200
				msg = "success"
	else:
		code = 202
		msg = 'access deny!'

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

