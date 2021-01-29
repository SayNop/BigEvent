from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm import load_only

from models import db
from models.category import Category
from utils.decorators import login_required
from utils import parser


class CategoryListResource(Resource):
    """
    频道列表
    """
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self):
        """
        获取所有频道信息
        """
        channels = Category.query.options(load_only(Category.id, Category.name, Category.alias, Category.is_delete))\
            .filter(Category.is_delete != Category.DELETE.DELETED).order_by(Category.id).all()

        results = []

        if not channels:
            return results

        for channel in channels:
            if channel.is_delete == Category.DELETE.NOPERMISSION:
                channel.is_delete = Category.DELETE.UNDELETE
            results.append({
                'id': channel.id,
                'name': channel.name,
                'alias': channel.alias,
                'is_delete': channel.is_delete
            })

        return {"status": 0, "message": '获取文章分类列表成功！', 'data': results}

    def post(self):
        """
        新增频道
        :return:
        """
        rp = RequestParser()
        rp.add_argument('name', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('alias', type=parser.regex(r'.+'), required=True, location='form')
        args = rp.parse_args()

        cate = Category.query.filter_by(name=args.name).first()

        if cate is not None:
            if cate.is_delete != Category.DELETE.DELETED:
                return {'status': 1, 'message': 'Category already exists.'}, 403
            else:
                # 已存在但被删除，恢复该分类
                cate.is_delete = Category.DELETE.UNDELETE
                cate.alias = args.alias
                db.session.add(cate)
                db.session.commit()
                return {"status": 0, "message": "新增文章分类成功！"}, 201

        # 不存在，新建分类
        cate = Category(name=args.name, alias=args.alias)
        db.session.add(cate)
        db.session.commit()

        return {"status": 0, "message": "新增文章分类成功！"}, 200


class CateDelResource(Resource):
    """操作单个频道数据"""
    method_decorators = {
        'get': [login_required]
    }

    def get(self, cate_id):
        """
        删除指定分类
        """
        cate = Category.query.filter_by(id=cate_id).first()

        if cate is None:
            return {'status': 1, 'message': 'Category does not exist.'}, 403

        # 不可被删除分类
        if cate.is_delete == Category.DELETE.NOPERMISSION:
            return {'status': 1, 'message': 'Category cannot be deleted.'}, 403

        # 删除该分类
        cate.is_delete = Category.DELETE.DELETED
        db.session.add(cate)
        db.session.commit()

        return {"status": 0, "message": "删除文章分类成功！"}, 200


class CategoryResource(Resource):
    """操作单个频道数据"""
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self, id):
        """获取指定分类信息"""
        cate = Category.query.filter_by(id=id).first()

        if cate is None:
            return {'status': 1, 'message': 'Category does not exist.'}, 403

        return {"msg": "获取文章分类数据成功！", 'id': cate.id, 'name': cate.name, 'alias': cate.alias,
                'is_delete': Category.DELETE.UNDELETE if cate.is_delete == Category.DELETE.NOPERMISSION
                else cate.is_delete}

    def post(self):
        """更新指定分类信息"""
        rp = RequestParser()
        rp.add_argument('id', type=parser.regex(r'\d+'), required=True, location='form')
        rp.add_argument('name', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('alias', type=parser.regex(r'.+'), required=True, location='form')
        args = rp.parse_args()

        cate = Category.query.filter_by(id=args.id).first()

        if cate is None:
            return {'status': 1, 'message': 'Category does not exist.'}, 403

        # 不可被删除分类
        if cate.is_delete == Category.DELETE.NOPERMISSION:
            return {'status': 1, 'message': 'Category cannot be modified.'}, 403

        if cate.is_delete == Category.DELETE.DELETED:
            return {'status': 1, 'message': 'Category has already be deleted.'}, 403

        cate.name = args.name
        cate.alias = args.alias
        db.session.add(cate)
        db.session.commit()
        return {"status": 0, "message": "更新分类信息成功！"}, 201
