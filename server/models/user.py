# -*- coding: utf-8 -*-
from server import log


class UserList(object):

    @staticmethod
    def get_user_list(cursor, page, limit, params):
        # 查询字段
        fields = '''
            shu_users.id,
            shu_user_profiles.user_name,
            shu_users.mobile,
            shu_user_profiles.user_type,
            -- 认证角色
            CASE WHEN 
                (SELECT auth_goods FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_goods_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_goods,
            CASE WHEN 
                (SELECT auth_driver FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_driver_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_driver,
            CASE WHEN 
                (SELECT auth_company FROM shu_user_auths
                 WHERE id = shu_user_profiles.last_auth_company_id
                 AND auth_status = 2
                 AND is_deleted != 1) = 1
                THEN 1 ELSE 0 END AS auth_company,
            -- 常驻地(暂定司机车辆认证地)
            (SELECT shm_regions.full_short_name
            FROM shu_vehicles, shu_vehicle_auths, shm_regions
            WHERE shu_vehicles.user_id = shu_users.id
            AND shu_vehicles.id = shu_vehicle_auths.vehicle_id
            AND auth_status = 2
            AND shu_vehicle_auths.home_station_county_id = shm_regions.`code`
            LIMIT 1) AS usual_city,
            -- 发货数
            (SELECT COUNT(*) FROM shf_goods WHERE shf_goods.user_id = shu_users.id) AS goods_count,
            -- 订单数
            (SELECT COUNT(*) FROM shb_orders WHERE shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id) AS order_count,
            -- 订单完成
            (SELECT COUNT(*) FROM shb_orders WHERE (shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id) AND shb_orders.`status` = 3) AS order_completed,
            -- 下载、注册渠道
            shu_user_profiles.download_channel,
            shu_user_profiles.from_channel,
            -- 最后登录
            FROM_UNIXTIME(shu_user_stats.last_login_time, '%Y-%m-%d') AS last_login_time,
            FROM_UNIXTIME(shu_users.create_time, '%Y-%m-%d') AS create_time'''

        command = """
            SELECT
            %s
            FROM shu_users
            LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
            LEFT JOIN shu_user_stats ON shu_users.id = shu_user_stats.user_id

            WHERE shu_users.is_deleted = 0
            """

        # 用户名
        if params['user_name']:
            command += 'AND shu_user_profiles.user_name = "%s" ' % params['user_name']
        # 手机号
        if params['mobile']:
            command += 'AND shu_users.mobile = "%s" ' % params['mobile']
        # 推荐人手机
        if params['reference_mobile']:
            command += 'AND shu_user_profiles.reference_id = (SELECT id FROM shu_users WHERE mobile = "%s") ' % params['reference_mobile']
        # 下载渠道
        if params['download_channel']:
            command += 'AND shu_user_profiles.download_channel = "%s" ' % params['download_channel']
        # 注册渠道
        if params['from_channel']:
            command += 'AND shu_user_profiles.from_channel = "%s" ' % params['from_channel']
        # 推荐注册
        if params['is_referenced'] == 1:
            command += 'AND shu_user_profiles.reference_id != 0 '
        elif params['is_referenced'] == 2:
            command += 'AND shu_user_profiles.reference_id = 0 '
        # TODO 常驻地(待议)
        if params['provinceid'] and params['cityid'] and params['regionid'] and params['townid']:
            pass

        # 注册角色
        if params['role_type'] == 1:
            command += 'AND shu_user_profiles.user_type = 1 '
        elif params['role_type'] == 2:
            command += 'AND shu_user_profiles.user_type = 2 '
        elif params['role_type'] == 3:
            command += 'AND shu_user_profiles.user_type = 3 '
        # 认证角色
        if params['role_auth'] == 1:
            command += '''
            AND (SELECT COUNT(*) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_goods_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_goods = 1) > 0 '''
        elif params['role_auth'] == 2:
            command += '''
            AND (SELECT COUNT(*) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_goods_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_driver = 1) > 0 '''
        elif params['role_auth'] == 3:
            command += '''
            AND (SELECT COUNT(*) FROM shu_user_auths
            WHERE shu_user_auths.id = shu_user_profiles.last_auth_goods_id AND shu_user_auths.auth_status = 2
            AND shu_user_auths.is_deleted = 0 AND shu_user_auths.auth_company = 1) > 0 '''
        # TODO 是否活跃(待议)
        if params['is_actived']:
            pass
        # 操作过
        if params['is_used'] == 1:
            command += 'AND (SELECT COUNT(*) FROM shf_goods WHERE shf_goods.user_id = shu_users.id) > 0 '
        elif params['is_used'] == 2:
            command += 'AND (SELECT COUNT(*) FROM shb_orders WHERE shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id) > 0 '
        elif params['is_used'] == 3:
            command += 'AND (SELECT COUNT(*) FROM shb_orders WHERE (shb_orders.owner_id = shb_orders.id OR shb_orders.driver_id = shb_orders.id) > 0 '
        # 贴车贴
        if params['is_car_sticker'] == 1:
            command += 'AND shu_user_profiles.trust_member_type = 2 AND ad_expired_time > UNIX_TIMESTAMP() '
        elif params['is_car_sticker'] == 2:
            command += 'AND shu_user_profiles.trust_member_type != 2 '
        # 最后登录
        if params['last_login_start_time'] and params['last_login_end_time']:
            command += 'AND shu_user_stats.last_login_time > %s AND shu_user_stats.last_login_time < %s ' % (
            params['last_login_start_time'], params['last_login_end_time'])
        # 注册日期
        if params['register_start_time'] and params['register_end_time']:
            command += 'AND shu_users.create_time > %s AND shu_users.create_time < %s ' % (
                params['register_start_time'], params['register_end_time'])

        # 总数
        user_count = cursor.query_one(command % 'COUNT(*) AS count')

        # 分页
        command += """
                    ORDER BY shu_user_stats.last_login_time DESC 
                    LIMIT %s, %s
                    """ % ((page - 1) * limit, limit)
        # 详情
        user_detail = cursor.query(command % fields)

        user_list = {
            'user_detail': user_detail if user_detail else [],
            'user_count': user_count['count'] if user_count['count'] else 0
        }
        log.info('user_list:{}'.format(user_list))

        return user_list


class UserStatistic(object):

    @staticmethod
    def get_user_statistic(cursor, params, user_id):
        command = """
        SELECT FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d') AS create_time, COUNT(*) AS count
        FROM shu_users
        LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id
        -- 认证
        INNER JOIN (
        SELECT
        shu_users.id,
        CASE WHEN
            (SELECT auth_goods FROM shu_user_auths
             WHERE id = shu_user_profiles.last_auth_goods_id
             AND auth_status = 2
             AND is_deleted != 1) = 1
            THEN 1 ELSE 0 END AS auth_goods,
        CASE WHEN
            (SELECT auth_driver FROM shu_user_auths
             WHERE id = shu_user_profiles.last_auth_driver_id
             AND auth_status = 2
             AND is_deleted != 1) = 1
            THEN 1 ELSE 0 END AS auth_driver,
        CASE WHEN
            (SELECT auth_company FROM shu_user_auths
             WHERE id = shu_user_profiles.last_auth_company_id
             AND auth_status = 2
             AND is_deleted != 1) = 1
            THEN 1 ELSE 0 END AS auth_company
        FROM shu_users
        LEFT JOIN shu_user_profiles ON shu_users.id = shu_user_profiles.user_id AND shu_user_profiles.is_deleted = 0
        WHERE shu_users.is_deleted = 0
        -- 认证、非认证
        ) AS auth ON shu_users.id = auth.id AND %(auth)s

        WHERE
        shu_users.is_deleted = 0
        -- 起始、终止时间
        AND shu_users.create_time >= :start_time
        AND shu_users.create_time < :end_time
        -- 角色
        %(role_type)s
        -- 地区
        %(region_user)s
        GROUP BY FROM_UNIXTIME(shu_users.create_time, '%%%%Y-%%%%m-%%%%d')
        """
        # 认证
        if params['is_auth'] == 1:
            auth = '(auth_goods = 1 OR auth_driver = 1 OR auth_company = 1)'
        elif params['is_auth'] == 2:
            auth = '(auth_goods = 0 AND auth_driver = 0 AND auth_company = 0)'
        else:
            auth = '1'
        # 角色类型
        if params['role_type'] == 1:
            role_type = 'AND shu_user_profiles.user_type = 1'
        elif params['role_type'] == 2:
            role_type = 'AND shu_user_profiles.user_type = 2'
        elif params['role_type'] == 3:
            role_type = 'AND shu_user_profiles.user_type = 3'
        else:
            role_type = 'AND 1'
        # 地区
        if params['region_id'] and user_id:
            region_user = 'AND shu_users.id IN (%s)' % ','.join(str(i) for i in user_id if i)
        elif params['region_id'] and not user_id:
            return []
        else:
            region_user = 'AND 1'

        command = command % {
            'auth': auth,
            'role_type': role_type,
            'region_user': region_user
        }

        user_statistic = cursor.query(command, {
            'start_time': params['start_time'],
            'end_time': params['end_time']
        })

        return user_statistic if user_statistic else []