from flask import request
from flask import jsonify
from app import db
from app.models import Student,Manager,Class,Teacher,Grade
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/list',methods = ['POST'])
@tokenUtils.token_required
def studentList(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}
	if role == 'manager' or role == 'teacher' or role == 'admin':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
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
						aStudent['email'] = student.email
						aStudent['tel'] = student.tel

						studentList.append(aStudent)
					data = studentList#{'studentList':studentList}
					code = 200
					msg = "success"

			else:
				studentListDB = Student.query.all();
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
		'code':code,
		'msg':msg,
		'result':data
	}
	return jsonify(json_to_send)

