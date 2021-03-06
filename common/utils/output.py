from flask import make_response, current_app, request
from flask_restful.utils import PY3
from json import dumps


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    # 改写默认的json响应方法，统一返回格式， 视图中只需返回：{数据}, 响应状态码
    if str(code) == '400':
        current_app.logger.warn(request.headers)
        current_app.logger.warn(request.data)
        current_app.logger.warn(str(data))

    # 去除系统响应的改造，使flask系统响应保持原状
    if 'status' not in data and 'msg' in data:
        data = {
            'status': 0,
            'message': data.pop('msg'),
            'data': data
        }

    # # 系统响应的改造
    # msg = data.pop('message')
    # if not data:
    #     data = {
    #         'status': 1,
    #         'message': msg
    #     }

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
