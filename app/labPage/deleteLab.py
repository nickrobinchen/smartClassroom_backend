from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Lab
from . import labPage

from app.auth import tokenUtils
import time 

@labPage.route('/lab/delete',methods = ['POST'])
@tokenUtils.token_required
def deleteLab(user_id,role):
	
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
			id = values.get('id')
			
			if id is None:
				code = 202
				msg = 'parameter error'
			else:
				lab = Lab.query.filter_by(id = id).first()
				if lab is not None:
					db.session.delete(lab)
					db.session.commit()

				code = 200
				msg = 'delete teacher success'
	else:
		code = 201
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

