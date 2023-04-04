from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Teacher,CourseForTeacher,Class,Course,Student
from . import coursePage

from app.auth import tokenUtils
import time 

@coursePage.route('/course/list',methods = ['GET'])
@tokenUtils.token_required
def list(user_id,role):
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager':
		manager = Manager.query.filter_by(id = user_id).first()
		if manager is None:
			code = 201
			msg = "none manager"
		else:
			courseListDB = Course.query.all();
			courseList = []
			index = 0
			for course in courseListDB:
				aCourse = {}
				index = index + 1
				aCourse['index'] = index
				aCourse['id'] = course.id
				aCourse['name'] = course.name
				aCourse['grade'] = course.grade
				courseList.append(aCourse)
			data = {'courseList':courseList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'result': {"items": courseList}
	}

	return jsonify(json_to_send)


@coursePage.route('/course/options',methods = ['GET'])
@tokenUtils.token_required
def options(user_id,role):

	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'teacher':
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			courseListDB = Course.query.all();
			courseList = []
			for course in courseListDB:
				aCourse = {}
				aCourse['value'] = course.id
				aCourse['label'] = course.name
				courseList.append(aCourse)
			data = {'courseOptions':courseList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)



@coursePage.route('/courseforteacher/list',methods = ['POST'])
@tokenUtils.token_required
def courseforteacherlist(user_id,role):

	teacher_id = user_id
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
			status = values.get('status') or 1

			courseForTeacherListDB = CourseForTeacher.query.filter_by(teacher_id=teacher_id,status=status).all()
			courseList = []
			index = 0
			for course in courseForTeacherListDB:
				aCourse = {}
				index = index + 1
				aCourse['index'] = index
				aCourse['id'] = course.id
				klass = Klass.query.filter_by(id=course.class_id).first()
				if klass is not None:
					aCourse['klass'] = klass.name
				_course = Course.query.filter_by(id=course.course_id).first()
				if _course is not None:
					aCourse['name'] = _course.name
				start_date_str = course.start_date.strftime('%Y-%m-%d')
				end_date_str = course.end_date.strftime('%Y-%m-%d')
				aCourse['startAndEndDate'] = start_date_str + " 至 " + end_date_str
				aCourse['week_date'] = course.week_date


				courseList.append(aCourse)

			data = {"courseList": courseList}
			code = 200
			msg = "course get success"
			

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)



@coursePage.route('/courseforstudent/list',methods = ['POST'])
@tokenUtils.token_required
def courseforstudentlist(user_id,role):

	student_id = user_id
	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'student':
		student = Student.query.filter_by(id = user_id).first()
		if student is None:
			code = 201
			msg = "none student"
		else:
			values = request.json
			status = values.get('status') or 1

			courseForTeacherListDB = CourseForTeacher.query.filter_by(klass_id=student.class_id, status=status).all()
			courseList = []
			index = 0
			for course in courseForTeacherListDB:
				aCourse = {}
				index = index + 1
				aCourse['index'] = index
				aCourse['id'] = course.id
				teacher = Teacher.query.filter_by(id=course.teacher_id).first()
				if teacher is not None:
					aCourse['teacher'] = teacher.name
				# klass = Klass.query.filter_by(id=course.klass_id).first()
				# if klass is not None:
				# 	aCourse['klass'] = klass.name
				_course = Course.query.filter_by(id=course.course_id).first()
				if _course is not None:
					aCourse['name'] = _course.name
				start_date_str = course.start_date.strftime('%Y-%m-%d')
				end_date_str = course.end_date.strftime('%Y-%m-%d')
				aCourse['startAndEndDate'] = start_date_str + " 至 " + end_date_str
				aCourse['week_date'] = course.week_date


				courseList.append(aCourse)

			data = {"courseList": courseList}
			code = 200
			msg = "course get success"
			

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)
