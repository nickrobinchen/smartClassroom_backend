from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Class,Teacher, Grade
from . import studentPage

from app.auth import tokenUtils
import time 

@studentPage.route('/student/classInfo',methods = ['GET'])
@tokenUtils.token_required
def classInfo(user_id,role):

	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager' or role == 'teacher' or role == 'admin':
		manager = Manager.query.filter_by(id = user_id).first()
		teacher = Teacher.query.filter_by(id = user_id).first()

		print(Grade.query.all())
		if manager is None and teacher is None:
			code = 201
			msg = "none manager or teacher"
		else:
			options = []
			collegeList = Class.query.with_entities(Class.belonged_college).distinct().all()
			if collegeList is not None:
				for item in collegeList:
					collegeInfo = {}
					college = item[0]
					collegeInfo['value'] = college
					collegeInfo['label'] = college

					gradeInfoList = []

					# gradeList = Class.query.with_entities(Class.belonged_grade).filter_by(belonged_college = college).distinct().all()
					# print(gradeList)
					gradeList = Grade.query.with_entities(Grade.grade_ref, Grade.id).all()
					print(gradeList)
					if gradeList is not None:
						for item in gradeList:
							gradeInfo = {}
							grade = item[0]
							gradeInfo['value'] = grade
							gradeInfo['label'] = grade

							classList = Class.query.with_entities(Class.name, Class.id).filter_by(belonged_college = college,belonged_grade = item[1]).all()
							if classList is not None:
								#print(classList)
								classInfoList = []
								for item in classList:
									classInfo = {}
									classInfo['value'] = item[1]
									classInfo['label'] = item[0]

									classInfoList.append(classInfo)

								gradeInfo['children'] = classInfoList

							if len(gradeInfo['children']):
								gradeInfoList.append(gradeInfo)

						collegeInfo['children'] = gradeInfoList

					options.append(collegeInfo)		


			data = {'classInfo':options}
			code = 200
			msg = "success"
	else:
		code = 202
		msg = 'access deny!'

	json_to_send = {
		'code':code,
		'msg':msg,
		'result':options
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
			collegeList = Class.query.with_entities(Class.belonged_college).distinct().all()
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


