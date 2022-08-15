import logging
from flask import Flask, jsonify
from flask_cors import CORS

from api import user_bp
from config import DB_CONNECT
from model import create_engine, init_panel_session, PanelSession


def init_mysql():
    """
    初始化数据库的配置信息
    """
    engine = create_engine(DB_CONNECT, pool_pre_ping=True, pool_recycle=1800, pool_size=10)
    init_panel_session(engine=engine)


def setting_logging(app):
    """
    日志的配置
    """
    app.logger.setLevel(logging.INFO)
    handler = logging.FileHandler("http.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)


def create_app():
    """
    采用工厂模，生成一个app实例子，避免循环导入问题
    """

    app = Flask(__name__)

    @app.teardown_request
    def on_teardown(*args):
        """
        采用钩子函数来自动移除连接的session 信息，
        """
        PanelSession.remove()

    # todo 写一个全局的日志（思路集合钩子函数来处理啊)

    # app实例一些信息的挂载
    init_mysql()
    setting_logging(app)
    app.register_blueprint(user_bp)
    CORS(app)

    return app
