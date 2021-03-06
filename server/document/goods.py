#!/usr/bin/python
# -*- coding:utf-8 -*-
# author=hexm

from flask_restplus import fields

from server import api
from server.status import APIStatus, FeedAPIStatus

request_goods_list_param = api.doc(params={
    'goods_id': '货源id',
    'mobile': '货主手机',
    'from_province_id': '发出地省份',
    'from_city_id': '发出地城市',
    'from_county_id': '发出地区县',
    'to_province_id': '目的地省份',
    'to_city_id': '目的地城市',
    'to_county_id': '目的地区县',
    'goods_type': '货源距离类型',
    'goods_price_type': '货源价格类型',
    'goods_status': '货源状态',
    'is_called': '是否通话',
    'vehicle_length': '车长要求',
    'vehicle_type': '车型要求',
    'node_id': '所属网点',
    'new_goods_type': '初次下单',
    'urgent_goods': '急需处理',
    'is_addition': '是否加价',
    'payment_method': '0:全部;1.发货人付;2.收货人付;3.省心保',
    'create_start_time': '发布开始日期',
    'create_end_time': '发布结束日期',
    'load_start_time': '装货开始日期',
    'load_end_time': '装货结束日期',
    'register_start_time': '注册开始时间',
    'register_end_time': '注册结束时间',
    'page': '页数',
    'limit': '条数',
}, description='货源统计列表查询参数')

response_success = api.response(200, '成功', api.model('response_success', {
    'state': fields.Integer(description=str(APIStatus.Ok)),
    'msg': fields.String(description=FeedAPIStatus.Decriptions[APIStatus.Ok]),
}))

request_cancel_reason_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'goods_type': '货源类型',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'region_id': '地区id'

}, description='取消货源原因查询参数')

request_goods_distribution_trend_param = api.doc(params={
    'start_time': '开始时间',
    'end_time': '结束时间',
    'periods': '时间周期,2:日，3:周，4:月，默认:2',
    'goods_type': '货源类型',
    'goods_price_type': '货源类型,1:议价,2:一口价,默认:0全部',
    'region_id': '地区id',
    'payment_method': '0:全部;1.发货人付;2.收货人付;3.省心保',
}, description='货源分布趋势查询参数')