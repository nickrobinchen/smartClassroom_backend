from flask import request
from flask import jsonify
from app import db
from app.models import Manager, Student, Teacher
# from . import studentPage

from app.auth import tokenUtils
from app.superApi import superApi


@superApi.route('/manager/list', methods=['GET'])
@tokenUtils.token_required
def managerList(user_id, role):
    managers = Manager.query.all()
    print(managers)
    json_to_send = {'code': 200, 'msg': 'success', 'result': list(
        map(lambda m: {'name': m.name, 'account': m.account, 'password': m.password}, managers))}
    return jsonify(json_to_send)


@superApi.route('/manager/add', methods=['POST'])
@tokenUtils.token_required
def managerAdd(user_id, role):
    json_to_send = {'code': 205, 'msg': 'error', 'result': 'Add manager failed.'}
    values = request.json
    print(values)
    if values['name'] and values['account']:
        manager = Manager(name=values['name'], account=values['account'],
                          password='manager' if values['password'] is None else values['password'])
        db.session.add(manager)
        db.session.commit()
        json_to_send = {'code': 200, 'msg': 'success', 'result': 'Add manager success.'}
    return jsonify(json_to_send)
