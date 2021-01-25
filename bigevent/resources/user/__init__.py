from flask import Blueprint
from flask_restful import Api

from . import passport, profile
from utils.output import output_json

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp, catch_all_404s=True)
user_api.representation('application/json')(output_json)

user_api.add_resource(passport.RegisterResource, '/api/reguser',
                      endpoint='Register')

user_api.add_resource(passport.LoginResource, '/api/login',
                      endpoint='Login')

user_api.add_resource(profile.UserInfoResource, '/my/userinfo',
                      endpoint='Userinfo')

user_api.add_resource(passport.ChangePwdResource, '/my/updatepwd',
                      endpoint='ChangePwd')
