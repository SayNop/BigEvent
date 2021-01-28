class DefaultConfig(object):
    """
    Flask默认配置
    """
    ERROR_404_HELP = False

    # flask-sqlalchemy使用的参数（因为远程连接下代码运行在开发环境中，因此使用127.0.0.1）
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/toutiao'  # 数据库
    SQLALCHEMY_BINDS = {
        'bj-m1': 'mysql://root:mysql@127.0.0.1:3306/bigevent',
        'bj-s1': 'mysql://root:mysql@127.0.0.1:8306/bigevent',
        'masters': ['bj-m1'],
        'slaves': ['bj-s1'],
        'default': 'bj-m1'
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 追踪数据的修改信号
    SQLALCHEMY_ECHO = True

    # JWT
    JWT_SECRET = 'Hty5fLbX7oyVq3Iu9v82@+YW1-8z*UvRnYTt4P6fdXc'
    JWT_EXPIRY_HOURS = 2
    JWT_REFRESH_DAYS = 14

    # 七牛云
    QINIU_ACCESS_KEY = 'nAKWN_5Ppz-CDlSn--3v1PhNYciy1NB6KJKlZJRx'
    QINIU_SECRET_KEY = 'd4np5uCyYdQUvk30-Hbpk-ZDamOQCr0irjSi-0Kh'
    QINIU_BUCKET_NAME = 'bigevent-test'
    QINIU_DOMAIN = 'qnnlgmzns.hd-bkt.clouddn.com/'

    # CORS
    # TODO 调试后要修改
    CORS_ORIGINS = '*'

    # Snowflake ID Worker 参数
    DATACENTER_ID = 0
    WORKER_ID = 0
    SEQUENCE = 0
