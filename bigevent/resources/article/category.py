from flask_restful import Resource
from sqlalchemy.orm import load_only

from models.category import Category
from utils.decorators import login_required


class CategoryResource(Resource):
    """
    频道列表
    """
    method_decorators = {
        'get': [login_required]
    }

    def get(self):
        """
        获取所有频道信息
        """
        channels = Category.query.options(load_only(Category.id, Category.name, Category.alias, Category.is_delete)) \
            .order_by(Category.id).all()

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

        return {'status':0, 'message': '获取文章分类列表成功！', 'data': results}
