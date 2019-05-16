from flask_restplus import Api, Resource
from app import app
from app.dal.db import search_user_by_name
from app.model.user import User
from app.model.pollLog import PollLog
from app.model.pollLog import PollLog

api = Api(app)

@api.route('/')
@api.route('/home')
class Hello(Resource):
    def get(self):
        return "welcome poll"


@api.route("/login")
class Login(Resource):
    def post(self):
        user_name = api.payload['user_name']
        password = api.payload['password']

@api.route("/register")
class Register(Resource):
    def post(self):
        user_name = api.payload['user_name']
        password = api.payload['password']
        check_password = api.payload['check_password']
        sex = api.payload['sex']
        if len(user_name) < 0 or len(password) == 0 or check_password != password:
            return "input error",400, {'Access-Control-Allow-Origin': '*'}
        user = search_user_by_name(user_name)
        if user is not None:
            return "user already exist", 400, {'Access-Control-Allow-Origin': '*'}
        else:
            pass

@api.route("/poll")
class Poll(Resource):
    def get(self):
        pass

    def post(self):
        pass


@api.route("/view/<string:poll_id>")
class View(Resource):
    def get(self, poll_id):
        pass


@api.route("/user")
class User(Resource):
    def get(self):
        pass


@api.route("/admin/user")
class Admin(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass

@api.route("/admin/poll")
class AdminPoll(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass









