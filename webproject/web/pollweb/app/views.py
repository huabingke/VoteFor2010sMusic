import os
from flask_restplus import Api, Resource, fields
from flask import Flask, session, render_template
from app.dal.db import *
from app.util.passwordUtil import create_salt, create_md5
from app.model.user import User
from app.model.pollInfo import PollInof
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
api = Api(app)



@api.route("/logout")
class Logout(Resource):
    def get(self):
        session.pop('username')
        return {"code": 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/login")
class Login(Resource):
    @api.expect(api.model('login_model', {
        'user_name': fields.String,
        'password': fields.String,
    }))
    def post(self):
        user_name = api.payload['user_name']
        password = api.payload['password']
        user = search_user_by_name(user_name)
        if user is None:
            return {"msg": "user is not exist", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            salt = user.salt
            if create_md5(password, salt) != user.password:
                return {"msg": "password is wrong", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                session['username'] = user.name
                return {"msg": "", "code": 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/register")
class Register(Resource):
    @api.expect(api.model('register_model', {
        'user_name': fields.String,
        'password': fields.String,
        'check_password': fields.String,
        'sex': fields.Integer
    }))
    def post(self):
        user_name = api.payload['user_name']
        password = api.payload['password']
        check_password = api.payload['check_password']
        sex = api.payload['sex']
        if len(user_name) < 0 or len(password) == 0 or check_password != password:
            return {"msg": "input error", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        user = search_user_by_name(user_name)
        if user is not None:
            return {"msg": "user already exist", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            salt = create_salt()
            password = create_md5(password, salt)
            user = User(user_name, password, sex, salt)
            insert_user_info(user)
            session['username'] = user.name
        return {'code': 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/session")
class Session(Resource):
    def get(self):
        name = session.get('username')
        if name is not None:
            return {'data':session.get('username')}
        else:
            return {'data':''}

def get_options(options):
    options_list = []
    poll_options_list = options.split(",")
    if len(poll_options_list) > 0:
        for id, des in enumerate(poll_options_list):
            options_list.append({'id':id,'des':des})
    return options_list

@api.route("/poll")
class Poll(Resource):
    def get(self):
        user_name = session.get('username')
        poll_infos = search_all_poll_info()
        if user_name is None:
            poll_datas = []
            for poll in poll_infos:
                poll_datas.append({'id': poll.id, 'name': poll.poll_name, 'options': get_options(poll.options), 'view': False})
        elif user_name == "admin":
            poll_datas = []
            for poll in poll_infos:
                poll_datas.append({'id': poll.id, 'name': poll.poll_name, 'options': get_options(poll.options), 'view': True})
        else:
            user = search_user_by_name(user_name)
            result = search_poll_by_user_id(user.id)
            poll_datas = []
            for poll in poll_infos:
                if poll.id in result.keys():
                    v = True
                else:
                    v = False
                poll_datas.append({'id': poll.id, 'name': poll.poll_name, 'options': get_options(poll.options), 'view': v})

        return {"data": poll_datas, "code": 0}, 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(api.model('poll_model', {
        'poll_id': fields.Integer,
        'select_id': fields.Integer,
        'user_name':fields.String
    }))
    def post(self):
        user_name = api.payload['user_name']
        user = search_user_by_name(user_name)
        if user is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            poll_id = api.payload['poll_id']
            select_id = api.payload['select_id']
            insert_poll_log(poll_id, user.id, user.sex, select_id)
            return {"code": 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/view/<int:poll_id>")
class View(Resource):
    def get(self, poll_id):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            name_list = search_poll_by_poll_id(poll_id)
            result, result_sex = search_poll_log_by_poll_id(poll_id, name_list)
        return {"result": result, "result_sex": result_sex, "code": 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/user")
class UserInfo(Resource):
    def get(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            user = search_user_by_name(user_name)
            if user is None:
                return {"msg": "user is not exist", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                return {"data":{"id": user.id, "name": user.name, "sex": user.sex}, "code":0}, 200, \
                       {'Access-Control-Allow-Origin': '*'}


@api.route("/admin/user")
class Admin(Resource):
    def get(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            user_infos = search_all_users()
            users = []
            for user in user_infos:
                if user.name != "admin":
                    users.append({'id': user.id, 'name': user.name, 'sex': user.sex})
            return {"data": users, "code": 0}, 200

    @api.expect(api.model('admin_add_user_model', {
        'user_name': fields.String,
        'password': fields.String,
        'sex': fields.Integer
    }))
    def post(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            name = api.payload['user_name']
            password = api.payload['password']
            sex = api.payload['sex']
            user = search_user_by_name(name)
            if user is not None:
                return {"msg": "user name  already exist", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                salt = create_salt()
                password = create_md5(password, salt)
                user = User(name, password, sex, salt)
                insert_user_info(user)
                return {"code": 0}, 200

    @api.expect(api.model('admin_delete_user_model', {
        'id': fields.Integer
    }))
    def delete(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            id = api.payload['id']
            delete_user_info(id)
            return {"code": 0}, 200, {'Access-Control-Allow-Origin': '*'}


@api.route("/admin/poll")
class AdminPoll(Resource):
    def get(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            poll_infos = search_all_poll_info()
            poll_datas = []
            for poll in poll_infos:
                poll_datas.append({'id': poll.id, 'name': poll.poll_name, 'options': get_options(poll.options)})
            return {'data': poll_datas, "code": 0}, 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(api.model('admin_add_poll_model', {
        'poll_name': fields.String,
        'options': fields.String
    }))
    def post(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            poll_name = api.payload['poll_name']
            options = api.payload['options']
            if len(poll_name) == 0 or len(options) == 0:
                return {"msg": "input is wrong", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
            else:
                l = list(set(options.split(',')))
                if len(l) <= 1:
                    return {"msg": "options input is wrong", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
                else:
                    s = ",".join(l)
                    poll_info = PollInof(poll_name,s)
                    insert_poll_info(poll_info)
                    return {"code": 0}, 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(api.model('admin_delete_poll_model', {
        'poll_id': fields.Integer,
    }))
    def delete(self):
        user_name = session.get('username')
        if user_name is None:
            return {"msg": "user is not login", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        elif user_name != 'admin':
            return {"msg": "user is not admin", "code": 1}, 200, {'Access-Control-Allow-Origin': '*'}
        else:
            poll_id = api.payload['poll_id']
            delete_poll_id(poll_id)
            delete_by_poll_id(poll_id)
            return {"code": 0}, 200, {'Access-Control-Allow-Origin': '*'}









