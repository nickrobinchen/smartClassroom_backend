from flask import request
from flask import jsonify
from app import db
from app.models import Manager,Lab
from . import labPage

from app.auth import tokenUtils
import time 

@labPage.route('/lab/edit',methods = ['POST'])
@tokenUtils.token_required
def editLab(user_id,role):
	
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
			name = values.get('name')
			
			if name is None or id is None:
				code = 202
				msg = 'parameter error'
			else:
				lab = Lab.query.filter_by(id = id).first()
				if lab is not None:
					lab.name = name
					
					db.session.add(lab)
					db.session.commit()

				code = 200
				msg = 'edit teacher success'
	else:
		code = 203
		msg = 'access deny'
	
	json_to_send = {
		'code':code,
		'msg':msg,
		'data':data
	}

	return jsonify(json_to_send)

