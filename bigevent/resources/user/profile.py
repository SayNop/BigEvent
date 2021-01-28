from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from utils import parser
from flask import g, current_app
from flask_restful import inputs
from sqlalchemy.exc import IntegrityError

from utils.decorators import login_required
from utils.qiniu_storage import upload
from models import db
from models.user import User


class UserInfoResource(Resource):
    """后台查看用户详情"""
    method_decorators = {
        'get': [login_required],
        'post': [login_required],
    }

    def get(self):
        """
        获取用户资料
        """
        user_id = g.user_id
        user = User.query.filter_by(id=user_id).first()
        result = {
            'msg': "获取用户基本信息成功！",
            'id': user_id,
            'username': user.username,
            'nickname': user.nickname,
            'email': user.email,
            'user_pic': user.user_pic
        }

        return result, 200

    def post(self):
        """
        更新用户的基本信息
        :return:
        """
        # 请求体参数：id、nickname、email
        json_parser = RequestParser()
        json_parser.add_argument('id', type=inputs.regex(r'^\d{19}$'), required=True, location='form')
        json_parser.add_argument('nickname', type=inputs.regex(r'^.{1,20}$'), required=True, location='form')
        json_parser.add_argument('email', type=parser.email, required=True, location='form')
        args = json_parser.parse_args()

        id = args.id
        # updata_value={
        #     'nickname': args.nickname,
        #     'email': args.email
        # }
        # print(updata_value)
        #
        # try:
        #     User.query.filter_by(id=id).update(updata_value)
        #     db.session.commit()
        # except IntegrityError:
        #     db.session.rollback()
        #     return {'status': 1, 'message': 'User name has existed.'}, 409

        user = User.query.get(id)
        if user is None:
            return {'status': 1, 'message': "该用户id不存在"}, 500
        user.nickname = args.nickname
        user.email = args.email
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {'status': 1, 'message': 'Username has existed.'}, 409

        return {'status': 0, 'message': "修改用户信息成功！"}, 201


class ChangePicResource(Resource):
    """修改头像"""
    method_decorators = {
        'post': [login_required]
    }

    def post(self):
        # 请求体参数：新头像，base64格式的字符串
        rp = RequestParser()
        rp.add_argument('avatar', type=parser.image_base64, required=True, location='form')
        args = rp.parse_args()

        user_id = g.user_id
        user = User.query.get(user_id)

        img = args.avatar

        try:
            user.user_pic = img
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"status": 1, 'message': 'Saving profile photo image failed.'}, 507

        return {"status": 0, "message": "更新头像成功！"}, 201
