import time

from flask_restful import abort

from server import log
from server.cache_data import init_regions
from server.meta.decorators import make_decorator, Response
from server.meta.session_operation import SessionOperationClass
from server.status import HTTPStatus, make_result, APIStatus
from server.utils.extend import compare_time, check_region_id


class HeatMap(object):

    @staticmethod
    @make_decorator
    def check_params(params):
        try:
            params['dimension'] = int(params.get('dimension', None) or 1)
            params['filter'] = params.get('filter', None) or 0
            params['field'] = int(params.get('field', None) or 1)
            params['start_time'] = int(params.get('start_time', None) or time.time() - 86400*7)
            params['end_time'] = int(params.get('end_time', None) or time.time())
            params['region_id'] = str(params.get('region_id', None) or '0')

            # 当前权限下所有地区
            if SessionOperationClass.check():
                role, locations_id = SessionOperationClass.get_locations()
                # 校验权限id
                if '区镇合伙人' in role or '网点管理员' in role or '城市经理' in role:
                    params['role_region_id'] = locations_id
                    L = []
                    if len(locations_id) > 1:
                        for i in locations_id:
                            level = init_regions.get_city_level(i)
                            L.append((level, i))
                        max_level, min_level = max(L, key=lambda k: k[0])[0], min(L, key=lambda k: k[0])[0]
                        if max_level == min_level:
                            params['authority_region_id'] = str(init_regions.get_parent_id(L[0][1]))
                            locations_id.append(params['authority_region_id'])
                            params['region_id'] = params['region_id'] if params['region_id'] != '0' else params['authority_region_id']
                        else:
                            L.sort(key=lambda item: item[0])
                            params['authority_region_id'] = L[0][1]
                            params['region_id'] = params['region_id'] if params['region_id'] != '0' else params['authority_region_id']
                    else:
                        params['authority_region_id'] = locations_id[0]
                        params['region_id'] = params['region_id'] if params['region_id'] != '0' else params['authority_region_id']
                elif role == '超级管理员':
                    params['role_region_id'] = locations_id + ['0']
                else:
                    params['role_region_id'] = ''
            else:
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.UnLogin, msg='请登录'))

            if not check_region_id(params['region_id'], params['role_region_id']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='地区参数非法'))

            if not compare_time(params['start_time'], params['end_time']):
                abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.BadRequest, msg='时间参数非法'))

            return Response(params=params)
        except Exception as e:
            log.error('error:{}'.format(e), exc_info=True)
            abort(HTTPStatus.BadRequest, **make_result(status=APIStatus.Forbidden, msg='拒绝请求'))
