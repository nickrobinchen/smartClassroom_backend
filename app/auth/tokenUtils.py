#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from itsdangerous import SignatureExpired,BadSignature
from config import Config
from functools import wraps
from flask import request
from flask import jsonify
from authlib.jose import jwt, JoseError

none_token = {
		'status':{
			'code':301,
			'msg':'none token'
		}
		}
expired_token = {
		'status':{
			'code':302,
			'msg':'expired token'
		},
		'data':{}
		}

bad_token = {
		'status':{
			'code':303,
			'msg':'bad token'
		},
		'data':{}
		}

#单位为s  一天过期
def gen_token(user,role,expiration=60*60*24):
	header = {'alg': 'HS256'}
	data = {'id':user.id,"role":role}
	return jwt.encode(header=header, payload=data,key = Config.SECRET_KEY)
	s = Serializer(Config.SECRET_KEY,expires_in = expiration)
	return s.dumps()


def token_required(func):
	@wraps(func)
	def wrapper(*args,**kwargs):

		kwargs['user_id'] = 1
		kwargs['role'] = 'manager'

		#return func(*args,**kwargs)

		token = request.headers.get('Authorization')
		if token is None:
			return jsonify(none_token)
		else:
			key = Config.SECRET_KEY

			try:
				data = jwt.decode(token, key)
			#except SignatureExpired:
			#	return jsonify(expired_token)
			except JoseError:
				return jsonify(bad_token)
			kwargs['user_id'] = data['id']
			kwargs['role'] = data['role']
		return func(*args,**kwargs)
	return wrapper

