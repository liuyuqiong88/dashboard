# -*- coding: utf-8 -*-
from server import api
from flask_restplus import fields


request_root_management_get = api.doc(params={
    'page': '页数',
    'limit': '条数',
})

request_root_management_add = api.doc(body=api.model('request_root_management_add', {
    'account': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'region_id': fields.String(description='所属地'),
}))

request_root_management_put = api.doc(body=api.model('request_root_management_put', {
    'account': fields.String(description='用户名'),
    'password': fields.String(description='密码'),
    'region_id': fields.String(description='所属地'),
}))

