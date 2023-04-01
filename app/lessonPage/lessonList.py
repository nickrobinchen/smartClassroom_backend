from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Lesson,Note,Record,Student,Teacher
from . import lessonPage

from app.auth import tokenUtils
import time 

@lessonPage.route('/lesson/list',methods = ['POST'])
@tokenUtils.token_required
def lessonList(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	courseforteacher_id = values.get('courseforteacher_id')

	if role == 'teacher' or 'student':
		teacher = Teacher.query.filter_by(id = user_id).first()
		student = Student.query.filter_by(id=user_id).first()
		if teacher is None and student is None:
			code = 201
			msg = "none teacher or student"
		else:
			lessonListDB = Lesson.query.filter_by(courseforteacher_id = courseforteacher_id).all();
			lessonList = []
			index = 0
			for lesson in lessonListDB:
				aLesson = {}
				index = index + 1
				aLesson['index'] = index
				aLesson['id'] = lesson.id
				aLesson['date'] = lesson.date.strftime('%Y-%m-%d')
				aLesson['week_date'] = lesson.week_date
				lessonList.append(aLesson)
			data = {'lessonList':lessonList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

