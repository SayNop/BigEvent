from flask_restful import Resource
from flask import g, current_app

from models import db
from models.user import User


class UserInfoResource(Resource):
    """后台查看用户详情"""

    def get(self):
        """
        获取用户资料
        """
        user_id = g.user_id
        user = User.query.filter_by(id=user_id).first()
        result = {
            'message':"获取用户基本信息成功！",
            'id': user_id,
            'username': user.username,
            'email': user.email,
            'user_pic': user.user_pic
        }

        return result, 200
