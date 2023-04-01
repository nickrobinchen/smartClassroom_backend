from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Lab
from . import labPage

from app.auth import tokenUtils
import time 

@labPage.route('/lab/list',methods = ['GET'])
@tokenUtils.token_required
def labList(user_id,role):

	code = 205
	msg = 'unknown error'
	data = {}

	if role == 'manager':
		manager = Manager.query.filter_by(id = user_id).first()
		if manager is None:
			code = 201
			msg = "none manager"
		else:
			labListDB = Lab.query.all();
			labList = []
			index = 0
			for lab in labListDB:
				aLab = {}
				index = index + 1
				aLab['index'] = index
				aLab['id'] = lab.id
				aLab['name'] = lab.name
				labList.append(aLab)
				
			data = {'labList':labList}
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

