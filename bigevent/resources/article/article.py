from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask import g, current_app
from sqlalchemy.orm import load_only

from models import db
from models.article import Article
from models.category import Category
from utils.decorators import login_required
from utils import parser
from utils.qiniu_storage import upload


class ArticleListResource(Resource):
    """
    文章列表
    """
    def post(self):
        """
        新增文章
        :return:
        """
        # 请求体参数：
        # title	是	string	文章标题
        # cate_id	是	int	所属分类 Id
        # content	是	string	文章内容
        # cover_img	是	blob二进制	文章封面
        # state
        rp = RequestParser()
        rp.add_argument('title', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('cate_id', type=parser.regex(r'\d+'), required=True, location='form')
        rp.add_argument('content', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('cover_img', type=parser.image_file, required=True, location='files')
        rp.add_argument('state', type=parser.article_state, required=True, location='form')
        args = rp.parse_args()

        user_id = g.user_id

        cate = Category.query.filter_by(id=args.cate_id).first()

        if cate is None:
            return {'status': 1, 'message': 'Category does not exist.'}, 403

        # 新建文章
        # try:
        #     photo_url = upload(args.avatar)
        # except Exception as e:
        #     # 日志（暂不记录）
        #     # current_app.logger.error('upload failed {}'.format(e))
        #     return {"status": 1, 'message': 'Uploading profile photo image failed.'}, 507
        art = Article(title=args.title, user_id=user_id, cate_id=args.cate_id, content=args.content,
                      # cover_img=photo_url,
                      status=Article.STATUS.DRAFT if args.state == '草稿' else Article.STATUS.APPROVED)
        db.session.add(art)
        db.session.commit()

        return {"status": 0, "message": "发布文章成功！"}, 200
