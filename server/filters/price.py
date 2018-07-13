from server.meta.decorators import make_decorator
from server.status import make_result, APIStatus, HTTPStatus


class PriceTrend(object):

    @staticmethod
    @make_decorator
    def get_result(params, data):
        # TODO 过滤参数

        return make_result(APIStatus.Ok, data=data), HTTPStatus.Ok