"""
function  : 1. 记录所有openid->id的键值对
            2. 记录用户 token -> user_id、session_id的键值对
            3. 记录 :phone::code:格式的 -> captcha_id的键值对
            4. 启动web服务的时候，初始化所有openid -> id的键值对
            5. 当redis不存在指定键值对时，会去mysql查询，并更新redis

desc      : openid -> id:   set  {service_name}:{table_name}:{openid}  10003(id)
            用户token       hset {service_name}:session:{token} user_id  100004  session_id 109304
            短信码          set  {service_name}:{phone}:{message_code} 109847
            手机号          set  {service_name}:phone:{phone} 100023(user_id)

datetime   :  2020-08-01

author     :  land

email      :  land@wintoo.com

©Witoo 2020 All rights reserved
"""

from config import APP_DEBUG
from redis import StrictRedis
from typing import Union
from shared import TOKEN_EXPIRE_TIME, DAY
from typing import Dict
import redis
import pickle
from util.date import get_ex_date


def _access_value(row, key: str):
    table = row.__tablename__
    prefix = table.lower()[:2]
    k1 = key
    k2 = f'{prefix}_{key}'
    if key == 'id':
        k1 = 'id'
        k2 = f'{prefix}id'
    if hasattr(row, k1):
        return getattr(row, k1)
    if hasattr(row, k2):
        return getattr(row, k2)


class RedisCache(object):
    
    conn: StrictRedis
    __service__ = 'ticket'

    def __init__(self, host=None, port=None, password=None, db=0):
        if host is not None and port is not None:
            self.conn = StrictRedis(host, port, db, password)
    
    def config(self, host, port, password, db, **kwargs):
        self.conn = StrictRedis(host, port, db, password, charset="utf-8", decode_responses=True, **kwargs)

    def init_cache(self, model, *args, **kwargs):
        """初始化指定数据表的所有openid -> id键值对

        *args与**kwargs支持接受Query.filter()与Query.filter_by()相同的参数，对初始化的数据行进行筛选

        Args:

            model(object): sqlalchemy中的mapper数据表，必须含有`__service__`与`__tablename__`这两个属性
        """
        service = model.__service__
        table = model.__tablename__
        openid = _access_value(model, 'openid')
        iid = _access_value(model, 'id')
        if openid is None:
            self._lookup_error(service, table, openid=openid)
        query = model.query
        if args:
            query = query.filter(*args)
        if kwargs:
            query = query.filter_by(**kwargs)

        elements = query.with_entities(openid, iid).all()

        print(f'init [{service}.{table}] with {len(elements)} elements')
        for i in range(0, len(elements), 500):
            # 每次最多只添加500条数据
            rows = elements[i: i + 500]
            key_values = {}
            for row in rows:
                openid = row[0]
                iid = row[1]
                key = f'{service}:{table}:{openid}'
                key_values[key] = iid

    def openid_to_id(self, model, openid: str) -> Union[int, None]:
        """将指定数据表的openid转为id

        当redis中没有指定`openid`的记录时，会去`model`表中查询，如果`model`中也没有记录，
        
        则会报`LookupError`

        Args:

            model(object): sqlalchemy中的mapper数据表，必须含有`__service__`与`__tablename__`这两个属性

            opend(str): openid

        Returns:

            iid(int): 整数id
        """
        service = model.__service__
        table = model.__tablename__
        key = f'{service}:{table}:{openid}'
        val = self.conn.get(key)
        if val is not None:
            return int(val)
        querier = {}
        prefix = table[:2]
        if hasattr(model, f'{prefix}_openid'):
            querier[f'{prefix}_openid'] = openid
        else:
            querier['openid'] = openid

        row = model.query.filter_by(**querier).scalar()
        if row is None:
            self._lookup_error(service, table, openid=openid)

        iid = _access_value(row, 'id')
        self.conn.set(key, iid)

        return int(iid)
    
    def set_openid(self, model, openid: str, iid: int):
        service = model.__service__
        table = model.__tablename__
        key = f'{service}:{table}:{openid}'
        self.conn.set(key, iid)

    def check_message_code(self, phone: str, code: str) -> Union[int, None]:
        """验证指定手机号`phone`与`code`是否正确，验证过后，该条数据就会被删除

        TODO:mysql容灾
        Args:

            phone(str):  手机号

            code(str):  验证码
        """
        key = f'{self.__service__}:{phone}:{code}'
        caid = self.conn.get(key)
        if caid is None:
            return
        self.conn.delete(key)
        return int(caid)
    
    def set_token(self, token: str, session_id: int, user_id: int):
        """为指定token设置session_id与user_id，并设置过期时间
        """
        key = f'{self.__service__}:session:{token}'
        mapping = {
            'user_id': user_id,
            'session_id': session_id
        }
        self.conn.hset(name=key, mapping=mapping)
        self.conn.expire(key, TOKEN_EXPIRE_TIME)

    def check_token(self, token: str) -> Dict[str, int]:
        """验证token的有效性，若redis中存在该token，则返回session_id与user_id

        注意：这一步的验证仅能确保在redis中存在该token，无法确保用户是否生成了新的token，

        因此还需要确保对应session的有效
        """
        key = f'{self.__service__}:session:{token}'
        mapping = self.conn.hgetall(name=key)
        if mapping is None:
            return
        user_id = mapping.get('user_id')
        session_id = mapping.get('session_id')
        if user_id is None or session_id is None:
            return
        return {
            'user_id': int(user_id),
            'session_id': int(session_id)
        }
    
    def init_user(self, model):
        """初始化所有用户的phone -> user_id
        """
        user_list = model.query.filter().all()
        for user in user_list:
            phone = _access_value(user, 'phone')
            uid = _access_value(user, 'id')
            key = f'{self.__service__}:phone:{phone}'
            self.conn.set(key, uid)
    
    def check_phone(self, model, phone: str):
        """登录或添加用户时可以快速验证是否存在指定手机的用户
        
        若用户存在，则会返回对应的user_id；反之则返回None
        """
        key = f'{self.__service__}:phone:{phone}'
        user_id = self.conn.get(key)
        if user_id is None:
            querier = {}
            ph_key = 'us_phone' if hasattr(model, 'us_phone') else 'phone'
            querier[ph_key] = phone
            user = model.query.filter_by(**querier).scalar()

            if user is None:
                return

            user_id = _access_value(user, 'id')
            self.conn.set(key, user_id)

        return int(user_id)

    def set_phone(self, phone, iid):
        key = f'{self.__service__}:phone:{phone}'
        self.conn.set(key, iid)

    def set_notify(self, user_id, date,  data):
        # 设定用户频道
        key = f'{self.__service__}:notify:{date}-{user_id}'
        all = self.conn.llen(key)
        if not all:
            self.conn.lpush(key, data)
            extime = get_ex_date(date)
            self.conn.expireat(key, extime)
        else:
            self.conn.lpush(key, data)
            
    def get_notify(self, user_id, date):
        # 设定用户频道
        key = f'{self.__service__}:notify:{date}-{user_id}'
        all = self.conn.llen(key)
        # 该键包含多少个元素
        return self.conn.lrange(key, 0, all)

    def del_notify(self):
        # TODO
        # 设定用户频道
        key = f'{self.__service__}:notify:210515'
        self.conn.delete(key)

    def _lookup_error(self, service, table, **kwargs):
        """生成异常的方法，方便快速排查错误
        """
        where = [f'{key}={val}' for key, val in kwargs.items()]
        where = ' ; '.join(where)
        msg = f'no record in [{service}.{table}] with {where}'
        raise LookupError(msg)

    def __getattribute__(self, name: str):
        attr = super(RedisCache, self).__getattribute__(name)
        if callable(attr) and APP_DEBUG and 'init' not in name:
            def func(*args, **kwargs):
                if APP_DEBUG:
                    print('-----' * 5)
                    print(f'before [RedisCache.{name}]: {args}')
                res = attr(*args, **kwargs)
                if APP_DEBUG:
                    print(f'after [RedisCache.{name}]: {res}')
                    print('-----' * 5)
                return res
            return func
        return attr

    def set_token_random(self, key, data):
        """
        设置token 与 6位 随机数字之间一一对应关系
        :param key:
        :param data:
        :return:
        """
        self.conn.set(key, data)

    def get_token_random(self, key):
        """
        获取token 与 6位 随机数字之间一一对应关系
        :param key:
        :return:
        """
        data = self.conn.get(key)
        if data is None:
            return None
        return data

    def has_key(self, key):
        """
        判断key是否存在
        :param key:
        :return:
        """
        ky = self.conn.exists(key)
        if ky:
            return 1
        return 0

    def remove_key(self, key):
        """
        回收对应的key
        :param key:
        :return:
        """
        self.conn.delete(key)


class Redisdata:
    """
    reids连接,用来缓存当天第一次数据库查询的数据,以此来加快接口的响应情况
    """

    connet: StrictRedis

    def __init__(self, host='192.168.1.101', port=6379, db=0, password=12345678):
        self.connet = redis.StrictRedis(host, port, db, password)

    def set_data(self, key, data, ex=86400):
        self.connet.set(key, pickle.dumps(data), ex)

    def get_data(self, key):
        data = self.connet.get(key)
        if data is None:
            return None

        return pickle.loads(data)
