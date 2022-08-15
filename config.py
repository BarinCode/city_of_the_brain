# import os

APP_DEBUG = False

# 版本控制
VERSION = 'v1'

# mysql数据库连接
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'panel_app'

DB_CONNECT = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# redis 数据库的连接
# RE_HOST = os.getenv('RE_HOST')
# RE_PORT = os.getenv('RE_PORT')
# RE_PASSWORD = os.getenv('RE_PASSWORD')
# RE_DB = os.getenv('RE_DB')

AMAP_KEY = '08390511ec386e6ed2c9b15c47cd00c8'
