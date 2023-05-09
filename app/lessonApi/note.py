from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Record,Student,Teacher,Note
from . import lessonPage

from app.auth import tokenUtils
from app.utils import fileHandle
import time 


@lessonPage.route('/note/list',methods = ['POST'])
@tokenUtils.token_required
def noteList(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.json
	lesson_id = values.get('lessonId')

	if role == 'teacher' or 'student' and lesson_id is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		student = Student.query.filter_by(id = user_id).first()
		if teacher is None and student is None:
			code = 201
			msg = "none teacher or student"
		else:
			noteListDB = Note.query.filter_by(lesson_id = lesson_id).all();
			noteList = []
			index = 0
			for note in noteListDB:
				aNote = {}
				index = index + 1
				aNote['index'] = index
				aNote['id'] = note.id
				aNote['name'] = note.name
				aNote['type'] = note.type
				aNote['md5_str'] = note.md5_str
				noteList.append(aNote)
			data = {'noteList':noteList}
			code = 200
			msg = "success"

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)


@lessonPage.route('/note/add',methods = ['POST'])
@tokenUtils.token_required
def addNote(user_id,role):
	
	code = 205
	msg = 'unknown error'
	data = {}

	values = request.form
	lesson_id = values.get('lessonId')

	files = request.files
	file = files.get('file')


	if role == 'teacher' and lesson_id is not None and file is not None:
		teacher = Teacher.query.filter_by(id = user_id).first()
		if teacher is None:
			code = 201
			msg = "none teacher"
		else:
			result = fileHandle.upload(file)
			name = result.get('name')
			type = result.get('type')
			md5_str = result.get('md5_str')

			note = Note(lesson_id,name,type,md5_str)
			db.session.add(note) 
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


@lessonPage.route('/note/delete',methods = ['POST'])
@tokenUtils.token_required
def deleteNote(user_id,role):
	
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
			id = values.get('id')
			
			if id is None:
				code = 202
				msg = 'parameter error'
			else:
				note = Note.query.filter_by(id = id).first()
				if note is not None:
					db.session.delete(note)
					db.session.commit()

				code = 200
				msg = 'delete note success'

	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)
