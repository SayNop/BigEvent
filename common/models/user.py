from datetime import datetime

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
    password = db.Column(db.String, doc='密码')
    nickname = db.Column(db.String, doc='昵称')
    email = db.Column(db.String, doc='邮箱')
    user_pic = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    status = db.Column(db.Integer, default=1, doc='状态，是否可用')