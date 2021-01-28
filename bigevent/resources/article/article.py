from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful import inputs
from flask import g, current_app
from sqlalchemy.orm import load_only, contains_eager

from models import db
from models.article import Article
from models.category import Category
from . import constants
from utils.decorators import login_required
from utils import parser
from utils.qiniu_storage import upload


class ArticleListResource(Resource):
    """
    文章列表
    """
    method_decorators = {
        'post': [login_required],
        'get': [login_required]
    }

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
        rp.add_argument('content', required=True, location='form')
        rp.add_argument('cover_img', type=parser.image_file, required=True, location='files')
        rp.add_argument('state', type=parser.article_state, required=True, location='form')
        args = rp.parse_args()

        cate = Category.query.filter_by(id=args.cate_id).first()
        if cate is None:
            return {'status': 1, 'message': 'Category does not exist.'}, 403
        if cate.is_delete == Category.DELETE.DELETED:
            return {'status': 1, 'message': 'The category has been deleted.'}, 403

        # 新建文章
        try:
            photo_url = upload(args.cover_img.read())
        except Exception as e:
            # 日志（暂不记录）
            # current_app.logger.error('upload failed {}'.format(e))
            return {"status": 1, 'message': 'Uploading profile photo image failed.'}, 507
        art = Article(title=args.title, user_id=g.user_id, cate_id=args.cate_id, content=args.content,
                      cover_img=photo_url,
                      status=Article.STATUS.DRAFT if args.state == '草稿' else Article.STATUS.APPROVED)
        db.session.add(art)
        db.session.commit()

        return {"status": 0, "message": "发布文章成功！"}, 200

    def get(self):
        """获取文章列表"""
        # 请求体参数：
        # pagenum	是	int	页码值
        # pagesize	是	int	每页显示多少条数据
        # cate_id	否	string	文章分类的 Id
        # state
        rp = RequestParser()
        rp.add_argument('pagenum', type=inputs.positive, required=True, location='args')
        rp.add_argument('pagesize', type=inputs.int_range(constants.DEFAULT_ARTICLE_PER_PAGE_MIN,
                                                          constants.DEFAULT_ARTICLE_PER_PAGE_MAX, 'per_page'),
                        required=True, location='args')
        rp.add_argument('cate_id', type=parser.regex(r'\d+'), required=False, location='args')
        rp.add_argument('state', type=parser.article_state, required=False, location='args')
        args = rp.parse_args()

        per_page = args.pagesize
        page = args.pagenum
        cate_id = None if args.cate_id is None else args.cate_id
        state = None if args.state is None else (Article.STATUS.DRAFT if args.state == '草稿' else
                                                 Article.STATUS.APPROVED)

        # 判断分类id是否合法
        if cate_id is not None:
            cate = Category.query.filter_by(id=args.cate_id).first()
            if cate is None:
                return {'status': 1, 'message': 'Category does not exist.'}, 403

        # 进行查询
        # 要响应的字段"Id","title","pub_date":"2020-01-03 12:19:57.690","state":"已发布","cate_name"
        if cate_id is None and state is None:
            # 查询cate_name需要通过cate_id联表查询
            arts = Article.query.join(Article.cate).options(load_only(Article.id, Article.title, Article.ctime,
                                                                      Article.status, Article.cate_id),
                                                            contains_eager(Article.cate).load_only(Category.name))\
                .filter(Article.is_delete == Article.DELETE.UNDELETE).order_by(Article.ctime.desc()).all()
        # 只过滤分类
        elif cate_id is None and state is not None:
            arts = Article.query.join(Article.cate).options(load_only(Article.id, Article.title, Article.ctime,
                                                                      Article.status, Article.cate_id),
                                                            contains_eager(Article.cate).load_only(Category.name))\
                .filter(Article.is_delete == Article.DELETE.UNDELETE, Article.status == state)\
                .order_by(Article.ctime.desc()).all()
        # 只过滤状态
        elif state is None and cate_id is not None:
            arts = Article.query.join(Article.cate).options(load_only(Article.id, Article.title, Article.ctime,
                                                                      Article.status, Article.cate_id),
                                                            contains_eager(Article.cate).load_only(Category.name))\
                .filter(Article.is_delete == Article.DELETE.UNDELETE, Article.cate_id == cate_id)\
                .order_by(Article.ctime.desc()).all()
        # 既要过滤分类，又要过滤状态
        else:
            arts = Article.query.join(Article.cate).options(load_only(Article.id, Article.title, Article.ctime,
                                                                      Article.status, Article.cate_id),
                                                            contains_eager(Article.cate).load_only(Category.name)) \
                .filter(Article.is_delete == Article.DELETE.UNDELETE, Article.status == state,
                        Article.cate_id == cate_id).order_by(Article.ctime.desc()).all()

        articles = []

        if not arts:
            return {"status": 0, "message": "获取文章列表成功！", "data": [], "total": 0}

        for art in arts:
            # "Id": 2,
            # "title": "666",
            # "pub_date": "2020-01-03 12:20:19.817",
            # "state": "已发布",
            # "cate_name": "股市"
            articles.append({
                'id': art.id,
                'title': art.title,
                'pub_date': art.ctime.strftime('%Y-%m-%d %H:%M:%s')[:-7],
                'state': '已发布' if art.status == Article.STATUS.APPROVED else '草稿',
                'cate_name': art.cate.name
            })

        # 通过结果列表切片进行分页
        page_articles = articles[(page - 1) * per_page:page * per_page]

        return {"status": 0, "message": "获取文章列表成功！", "data": page_articles, "total": len(articles)}


class ArticleDelResource(Resource):
    """删除文章数据"""
    method_decorators = {
        'get': [login_required]
    }

    def get(self, id):
        """
        删除指定分类
        """
        art = Article.query.filter_by(id=id).first()

        if art is None:
            return {'status': 1, 'message': 'The article does not exist.'}, 403

        # 删除该文章
        art.is_delete = Article.DELETE.DELETED
        db.session.add(art)
        db.session.commit()

        return {"status": 0, "message": "删除文章成功！"}, 200


class ArticleResource(Resource):
    """操作单个文章数据"""
    method_decorators = {
        'get': [login_required],
        'post': [login_required]
    }

    def get(self, id):
        """获取指定文章信息"""
        art = Article.query.filter_by(id=id).first()

        if art is None:
            return {'status': 1, 'message': 'The article does not exist.'}, 403

        # 返回字段："Id", "title", "content", "cover_img", "pub_date", "state", "is_delete": 0, "cate_id", "author_id"
        return {'msg': '获取文章分类数据成功！', 'id': art.id, 'title': art.title, 'content': art.content,
                'cover_img': None if art.cover_img is None else current_app.config['QINIU_DOMAIN'] + art.cover_img,
                'pub_date': art.ctime.strftime('%Y-%m-%d %H:%M:%s')[:-7],
                "state": '已发布' if art.status == Article.STATUS.APPROVED else '草稿', 'is_delete': art.is_delete,
                'cate_id': art.cate_id, 'author_id': art.user_id,}

    def post(self):
        """更新指定文章信息"""
        # 请求参数：Id	title	cate_id content	cover_img	state
        rp = RequestParser()
        rp.add_argument('id', type=parser.regex(r'\d+'), required=True, location='form')
        rp.add_argument('title', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('cate_id', type=parser.regex(r'.+'), required=True, location='form')
        rp.add_argument('content', required=True, location='form')
        rp.add_argument('cover_img', type=parser.image_file, required=True, location='files')
        rp.add_argument('state', type=parser.regex(r'.+'), required=True, location='form')
        args = rp.parse_args()

        # 判断文章状态
        art = Article.query.filter_by(id=args.id).first()
        if art is None:
            return {'status': 1, 'message': 'The article does not exist.'}, 403
        if art.is_delete == Article.DELETE.DELETED:
            return {'status': 1, 'message': 'The article has been deleted.'}, 403
        if art.user_id != g.user_id:
            print(f'art.user_id is {art.user_id}, g.user_id is {g.user_id}')
            return {'status': 1, 'message': 'You have no permission to change this article.'}, 403

        # 判断分类状态
        cate = Category.query.filter_by(id=args.cate_id).first()
        if cate is None:
            return {'status': 1, 'message': 'The category does not exist.'}, 403
        if cate.is_delete == Category.DELETE.DELETED:
            return {'status': 1, 'message': 'The category has been deleted.'}, 403

        # 上传图片
        try:
            photo_url = upload(args.cover_img.read())
        except Exception as e:
            # 日志（暂不记录）
            # current_app.logger.error('upload failed {}'.format(e))
            return {"status": 1, 'message': 'Uploading profile photo image failed.'}, 507
        art.title = args.title
        art.cate_id = args.cate_id
        art.content = args.content
        art.cover_img=photo_url
        art.status = Article.STATUS.DRAFT if args.state == '草稿' else Article.STATUS.APPROVED
        db.session.add(art)
        db.session.commit()

        return {"status": 0, "message": "修改文章成功！"}, 201
