from datetime import datetime

from . import db


class Category(db.Model):
    """
    新闻频道
    """
    __tablename__ = 'tb_cate'

    class DELETE:
        NOPERMISSION = 2  # 不可删除
        DELETED = 1  # 已删除
        UNDELETE = 0  # 未删除

    id = db.Column('cate_id', db.Integer, primary_key=True, doc='频道ID')
    name = db.Column('cate_name', db.String, doc='频道名称')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')
    alias = db.Column(db.String, doc='别名')
    is_delete = db.Column(db.Integer, default=0, doc='是否删除')