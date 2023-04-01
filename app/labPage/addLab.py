from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Lab
from . import labPage

from app.auth import tokenUtils
import time 

@labPage.route('/lab/add',methods = ['POST'])
@tokenUtils.token_required
def addLab(user_id,role):
	
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

			if name is None:
				code = 202
				msg = 'parameter error'
			else:
				lab = Lab(name)
				db.session.add(lab) 
				db.session.commit()

				code = 200
				msg = 'success'
	else:
		code = 203
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

