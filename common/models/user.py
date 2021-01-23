from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model):
    """
    用户信息
    """
    __tablename__ = 'tb_user'

    class STATUS:
        ENABLE = 1  # 可用
        DISABLE = 0 # 不可用

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    username = db.Column(db.String, doc='登陆用户名')
    _password = db.Column('password', db.String, doc='密码')
    nickname = db.Column(db.String, doc='昵称')
    email = db.Column(db.String, doc='邮箱')
    user_pic = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    status = db.Column(db.Boolean, default=1, doc='状态，是否可用')

    @property
    def password(self):
        raise Exception('密码不能被读取')  # 为了保持使用习惯，还是设置一个password字段用来设置密码，当然也不能被读取。

    # 赋值password，则自动加密存储。
    @password.setter
    def password(self, value):
        self._password_hash_ = generate_password_hash(value)

    # 使用check_password,进行密码校验，返回True False。
    def check_password(self, pasword):
        return check_password_hash(self._password_hash_, pasword)
