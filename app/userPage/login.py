from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Teacher,Student
from . import userPage

from app.auth import tokenUtils
import time 

@userPage.route('/user/test',methods = ['GET'])
def test():
	user = Manager.query.all()
	return 'test success test!'

@userPage.route('/user/login',methods = ['POST'])
def login():
	code = 205
	msg = 'success'
	data = {}

	values = request.json
	account = values.get('account')
	password = values.get('password')
	print(values)
	if account is None or password is None:
		code = 201
		msg = 'there is no account or password!'
	else:
		role = ""
		first = account[0:1]
		user = None
		if first == "M":
			user = Manager.query.filter_by(account = account).first()
			role = "manager"
		elif first == "U":
			user = Student.query.filter_by(account = account).first()
			role = "student"
		elif first == "T":
			user = Teacher.query.filter_by(account = account).first()
			role = "teacher"

		if user is None:
			code = 202
			msg = '账号不存在'
		else:
			if user.password != password:
				code = 203
				msg = 'password error!'
			else:
				code = 200
				data = {
						'roles':[role],
						'token':tokenUtils.gen_token(user,role).decode('ascii'),
						'expire_time':int(round(time.time()*1000+60*60*24*1000))
					}
	json_to_send = {
		'code':code,
		'msg':msg,
		'result':data
	}
	print(json_to_send)
	return jsonify(json_to_send)


@userPage.route('/user/getInfo',methods = ['GET'])
@tokenUtils.token_required
def getUserInfo(user_id, role):
	code = 205
	msg = 'success'
	data = {}
	user = None
	print((user_id, role))
	if role == "manager" or role == "admin":
		user = Manager.query.filter_by(id=user_id).first()
	elif role == "teacher":
		user = Student.query.filter_by(id=user_id).first()
	elif role == "student":
		user = Teacher.query.filter_by(id=user_id).first()
	code = 200
	data = dict(roles=[dict(roleName=role,value=role)],userId=user_id,username=user.name,realName=user.name,avatar='')
	json_to_send = {
		'code':code,
		'msg':msg,
		'result': data
	}
	print(json_to_send)
	return jsonify(json_to_send)

@userPage.route('/modifyPassword',methods=['POST'])
@tokenUtils.token_required
def change_password(user_id):
	values = request.json
	pre_password = values.get('prevPwd')
	new_password = values.get('newPwd')

	return 'success'