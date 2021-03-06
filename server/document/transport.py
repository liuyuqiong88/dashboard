from server import api

transport_radar_param = api.doc(params={
    "start_time": "开始时间",
    "end_time": "开始时间",
    "region_id": "地区id",
    "from_city_id": "出发地城市id",
    "from_county_id": "出发地区县id",
    "to_city_id": "目的地城市id",
    "to_county_id": "目的地区县id",
}, description='运力趋势查询参数')

transport_list_param = api.doc(params={
    "from_city_id": "出发地城市id",
    "to_city_id": "目的地城市id",
    "start_time": "统计开始时间,默认传当前选择日期00:00:00的时间戳",
    "end_time": "统计结束时间,默认传当前时间戳",
    "calc_town": "0:不计算区镇;1:计算出发地城市下所有区镇;2.计算目的地城市下所有区镇;3.同时计算出发地和目的地城市下所有区镇",
    "page": "页数",
    "limit": "条数",
}, description='运力列表查询参数')
