from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Teacher
from . import teacherPage

from app.auth import tokenUtils
import time 

@teacherPage.route('/teacher/add',methods = ['POST'])
@tokenUtils.token_required
def addTeacher(user_id,role):

	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager':
		manager = Manager.query.filter_by(id = user_id).first()
		if manager is None:
			code = 201
			msg = "none manager"
		else:
			values = request.json
			name = values.get('name')
			account = values.get('account')
			tel = values.get('tel')
			email = values.get('email')
			address = values.get('address')

			if name is None or account is None:
				code = 202
				msg = 'parameter error'
			else:
				try:
					password = 'teacher'#account[-6:]
					teacher = Teacher(name,account,tel,address,email,password)
					db.session.add(teacher) 
					db.session.commit()

					code = 200
					msg = 'success'
				except:
					pass		
	else:
		code = 202
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'message':msg,
		'result': data
	}

	return jsonify(json_to_send)

