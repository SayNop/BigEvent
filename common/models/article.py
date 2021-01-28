from datetime import datetime

from . import db
from .category import Category


class Article(db.Model):
    """
    文章基本信息表
    """
    __tablename__ = 'tb_article'

    class STATUS:
        APPROVED = 1  # 已发布
        DRAFT = 0  # 草稿

    class DELETE:
        DELETED = 1  # 已删除
        UNDELETE = 0  # 未删除

    id = db.Column('article_id', db.Integer, primary_key=True,  doc='文章ID')
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.user_id'), doc='用户ID')
    cate_id = db.Column(db.Integer, db.ForeignKey('tb_cate.cate_id'), doc='分类ID')
    title = db.Column(db.String, doc='标题')
    content = db.Column(db.Text, doc='帖文内容')
    cover_img = db.Column(db.String, doc='封面')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    status = db.Column(db.Integer, default=0, doc='帖文状态')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, doc='更新时间')
    is_delete = db.Column(db.Boolean, default=False, doc='是否删除')

    cate = db.relationship('Category', primaryjoin='Article.cate_id==foreign(Category.id)', uselist=False)

