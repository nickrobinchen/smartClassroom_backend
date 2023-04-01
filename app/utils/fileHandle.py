from . import utils
from flask import jsonify,request,send_from_directory
import os,hashlib,time

def upload(file):
	result = {}
	if file is not None:
		filedir = os.path.join(os.getcwd(),"file")
		filename = file.filename
		type = filename.split('.')[1]
		name = filename.split('.')[0]
		md5_str = genMD5(name + str(time.time()))

		savepath = os.path.join(filedir,md5_str + '.' + type)
		file.save(savepath)

		result['type'] = type
		result['name'] = name
		result['md5_str'] = md5_str
		
	return result

@utils.route("/download",methods=['POST'])
def download():
	filename = request.json.get('filename')
	dirpath = os.path.join(os.getcwd(), 'file')  
	return send_from_directory(dirpath, filename, as_attachment=True)
    

def genMD5(str):
	
    hl = hashlib.md5()

    hl.update(str.encode(encoding='utf-8'))

    return hl.hexdigest()[0:8]
