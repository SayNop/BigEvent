from flask_restful import Resource
from flask import current_app
from flask_restful.reqparse import RequestParser
from datetime import datetime
from redis.exceptions import ConnectionError

from utils import parser
from models import db
from models.user import User


class RegisterResource(Resource):
    """
    认证
    """
    def post(self):
        """
        登录创建token
        """
        json_parser = RequestParser()
        json_parser.add_argument('username', type=parser.regex(r'.+'), required=True, location='form')
        json_parser.add_argument('password', type=parser.regex(r'.+'), required=True, location='form')
        args = json_parser.parse_args()
        username = args.username
        password = args.password

        # 查询或保存用户
        user = User.query.filter_by(username=username).first()

        if user is None:
            # 用户不存在，注册用户
            # 采用雪花算法生成分布式id
            # 其他会用到雪花算法生成id的地方：文章id 评论id
            # 这三个id在代码中直接操作数据库使用，所以要全局唯一，使用雪花算法生成
            user_id = current_app.id_worker.get_id()
            user = User(id=user_id, username=username, password=password, nickname=username, last_login=datetime.now())
            db.session.add(user)
            db.session.commit()
        else:
            if user.status == User.STATUS.DISABLE:
                return {'status': 1, 'message': 'Invalid user.'}, 403
            else:
                return {'status':1, 'message':'User already exists.'}, 403

        return {"status": 0,"message": "注册成功！"}, 200









