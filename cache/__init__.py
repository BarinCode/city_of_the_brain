# from .cache import RedisCache, Redisdata
# import redis
# import pickle
# from panel_app.config import RE_HOST, RE_PORT
# from panel_app.res import make_error, ResponseCode
#
# redis_cache = RedisCache()
#
# redis_data = Redisdata()
#
#
# def init_redis(host, port, password, db=0):
#     print(f'[INFO] build redis connection with {RE_HOST}:{RE_PORT}')
#     redis_cache.config(host=host, port=port, password=password, db=db)
#
#
# def fetch_resource(model, openid, reference=None, **kwargs):
#     """将redis于mysql服务结合的方法，通过该方法，可以获取指定
#
#     数据表model、指定openid的数据行，当reference不为None的时候，
#
#     仅获取指定公司的数据。若没有找到对应的数据行，则会报`resource not found`
#     """
#     iid = redis_cache.openid_to_id(model, openid)
#     if iid is not None:
#         prefix = model.__tablename__[:2]
#         querier = {
#             f"{prefix}id": iid,
#             f"{prefix}_status": 1
#         }
#         if reference is not None:
#             querier[f"{prefix}_reference"] = reference
#
#         if kwargs is not None:
#             querier.update(kwargs)
#         resource = model.query.filter_by(**querier).scalar()
#         if not resource:
#             make_error(ResponseCode.unauthorized)
#         return resource
#
#     make_error(ResponseCode.resource_not_found)
