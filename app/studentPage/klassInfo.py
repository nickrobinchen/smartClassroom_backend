from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Klass,Teacher
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/klassInfo',methods = ['GET'])
@tokenUtils.token_required
def klassInfo(user_id,role):

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
			options = []
			collegeList = Klass.query.with_entities(Klass.belonged_college).distinct().all()
			if collegeList is not None:
				for item in collegeList:
					collegeInfo = {}
					college = item[0]
					collegeInfo['value'] = college
					collegeInfo['label'] = college

					gradeInfoList = []

					gradeList = Klass.query.with_entities(Klass.belonged_grade).filter_by(belonged_college = college).distinct().all()
					if gradeList is not None:
						for item in gradeList:
							gradeInfo = {}
							grade = item[0]
							gradeInfo['value'] = grade
							gradeInfo['label'] = grade

							klassList = Klass.query.with_entities(Klass.name).filter_by(belonged_college = college,belonged_grade = grade).all()
							if klassList is not None:
								klassInfoList = []
								for item in klassList:
									klassInfo = {}
									klass = item[0]
									klassInfo['value'] = klass
									klassInfo['label'] = klass

									klassInfoList.append(klassInfo)

								gradeInfo['children'] = klassInfoList

							gradeInfoList.append(gradeInfo)

						collegeInfo['children'] = gradeInfoList

					options.append(collegeInfo)		


			data = {'klassInfo':options}
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


@studentPage.route('/student/collegeInfo',methods = ['GET'])
@tokenUtils.token_required
def collegeInfo(user_id,role):
	
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
			options = []
			collegeList = Klass.query.with_entities(Klass.belonged_college).distinct().all()
			if collegeList is not None:
				for item in collegeList:
					collegeInfo = {}
					college = item[0]
					collegeInfo['value'] = college
					collegeInfo['label'] = college

					options.append(collegeInfo)		


			data = {'collegeInfo':options}
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


