from flask import Blueprint
from flask_restful import Api

from . import category, article
from utils.output import output_json


article_bp = Blueprint('article', __name__)
article_api = Api(article_bp, catch_all_404s=True)
article_api.representation('application/json')(output_json)


article_api.add_resource(category.CategoryListResource, '/my/article/cates',
                      endpoint='Category')

article_api.add_resource(category.CategoryListResource, '/my/article/addcates',
                      endpoint='addCategory')

article_api.add_resource(category.CateDelResource, '/my/article/deletecate/<int:id>',
                      endpoint='delCategory')

article_api.add_resource(category.CategoryResource, '/my/article/cates/<int:id>',
                      endpoint='getSCategory')

article_api.add_resource(category.CategoryResource, '/my/article/updatecate',
                         endpoint='updateCategory')

article_api.add_resource(article.ArticleListResource, '/my/article/add',
                         endpoint='addArticle')

article_api.add_resource(article.ArticleListResource, '/my/article/list',
                         endpoint='ArticleList')

article_api.add_resource(article.ArticleDelResource, '/my/article/delete/<int:id>',
                         endpoint='delArticle')