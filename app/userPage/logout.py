from app.auth import tokenUtils
from flask import jsonify
from app.models import Manager
from . import userPage

@userPage.route('/logout',methods = ['POST'])
@tokenUtils.token_required
def logout(user_id):
	json_to_send = {
		
		'status':
		{
			'code':200,
			'msg':'logout success!'
		},
		
		'data':{}
	}
		
	return jsonify(json_to_send)