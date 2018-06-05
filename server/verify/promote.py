import time

from flask_restful import abort

from server import log
from server.meta.decorators import make_decorator, Response
from server.status import HTTPStatus, make_result, APIStatus


class PromoteEffect(object):

    @staticmethod
    @make_decorator
    def check_params(page, limit, params):

        try:
            # 通过params获取参数，获取不到就赋予默认值
            user_name = params.get('user_name', '')
            mobile = params.get('mobile', '')
            region_id = int(params.get('region_id', 0))
            role_type = int(params.get('role_type', 0))
            goods_type = int(params.get('goods_type', 0))
            is_actived = int(params.get('is_actived', 0))
            is_car_sticker = int(params.get('is_car_sticker', 0))
            start_time = int(params.get('start_time', 0))
            end_time = int(params.get('end_time', 0))

            # 判断时间是否合法
            if start_time and end_time:
                if start_time < end_time < time.time():
                    pass
                else:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间有误'))

            # 构造请求参数
            params = {
                'user_name': user_name,
                'mobile': mobile,
                'region_id': region_id,
                'role_type': role_type,
                'goods_type': goods_type,
                'is_actived': is_actived,
                'is_car_sticker': is_car_sticker,
                'start_time': start_time,
                'end_time': end_time
            }

            return Response(page=page, limit=limit, params=params)

        except Exception as e:
            log.error('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='参数有误'))


class PromoteQuality(object):

    @staticmethod
    @make_decorator
    def check_params(params):

        try:
            # 校验参数
            start_time = int(params.get('start_time')) if params.get('start_time') else time.time() - 8 * 60 * 60 * 24
            end_time = int(params.get('end_time')) if params.get('end_time') else time.time() - 60 * 60 * 24
            periods = int(params.get('periods')) if params.get('periods') else 2
            dimension = int(params.get('dimension')) if params.get('dimension') else 1
            type = int(params.get('type')) if params.get('type') else 1
            region_id = int(params.get('region_id')) if params.get('region_id') else 0

            # TODO 验证参数
            if start_time and end_time:
                if start_time < end_time < time.time():
                    pass
                else:
                    abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))
            elif not start_time and not end_time:
                pass
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数有误'))

            params = {
                'start_time': start_time,
                'end_time': end_time,
                'periods': periods,
                'dimension': dimension,
                'type': type,
                'region_id': region_id,
            }

            return Response(params=params)
        except Exception as e:
            log.warn('Error:{}'.format(e))
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='请求参数非法'))
