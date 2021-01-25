from flask_restful import Resource
from flask import g, current_app
from flask_restful.reqparse import RequestParser
from datetime import datetime, timedelta

from utils import parser
from models import db
from models.user import User
from utils.jwt_util import generate_jwt
from utils.decorators import login_required


class RegisterResource(Resource):
    """
    注册
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

        return {"status": 0, "message": "注册成功！"}, 200


class LoginResource(Resource):
    """
    登陆
    """
    def _generate_tokens(self, user_id, refresh=True):
        """
        生成token 和refresh_token
        :param user_id: 用户id
        :return: token, refresh_token
        """
        # 颁发JWT
        secret = current_app.config['JWT_SECRET']
        # 生成调用token， refresh_token
        expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])

        token = generate_jwt({'user_id': user_id}, expiry, secret)

        if refresh:
            exipry = datetime.utcnow() + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])
            refresh_token = generate_jwt({'user_id': user_id, 'is_refresh': True}, exipry, secret)
        else:
            refresh_token = None

        return token, refresh_token

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
            return {'status':1, 'message':'User doest not exists.'}, 403
        else:
            if user.status == User.STATUS.DISABLE:
                return {'status': 1, 'message': 'Invalid user.'}, 403


        # 登陆业务逻辑
        if user.check_password(password):
            token, refresh_token = self._generate_tokens(user.id, False)
        else:
            return {'status': 1, 'message': 'Wrong password.'}, 403

        return {'msg': '登录成功！', 'token': 'Bearer '+token}, 201


class ChangePwdResource(Resource):
    """修改密码"""
    method_decorators = {
        'post': [login_required]
    }

    def post(self):
        """修改密码"""
        # 请求体参数：oldPwd、newPwd
        json_parser = RequestParser()
        json_parser.add_argument('oldPwd', type=parser.regex(r'.+'), required=True, location='form')
        json_parser.add_argument('newPwd', type=parser.regex(r'.+'), required=True, location='form')
        args = json_parser.parse_args()
        oldPwd = args.oldPwd
        newPwd = args.newPwd

        user_id = g.user_id
        user = User.query.get(user_id)

        # 校验密码
        if not user.check_password(oldPwd):
            return {'status': 1, 'message': 'Wrong password.'}, 403

        # 提交到数据库执行
        user.password = newPwd
        db.session.add(user)
        db.session.commit()

        return {"status": 0, "message": "更新密码成功！"}, 201



