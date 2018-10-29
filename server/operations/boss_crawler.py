# -*- coding: utf-8 -*-
import random

import requests
from lxml import etree

from server.configs import CITY_CODE, USER_AGENTS


def boss_spider(params):
    job_name = params.pop("job_name")
    region = params.pop("region")
    time_scale = params.pop("time_scale")
    page = params.pop("page")

    if region:
        region = CITY_CODE.get(region)
        if not region: region = 100010000
    else:
        region = 100010000
    while True:
        url = "https://www.zhipin.com/c{}/?query={}&page={}&period={}".format(region, job_name, page, time_scale)

        headers = {"User-Agent": random.choice(USER_AGENTS)}

        response = requests.get(url=url, headers=headers)

        data = response.content.decode()
        data = data.replace('<em class="vline"></em>', ',')
        data = etree.HTML(data)

        node_list = data.xpath('//div[@class="job-list"]//ul/li')

        events = []

        for node in node_list:

            job_name = node.xpath('./div/div[1]/h3/a/div[1]/text()')[0]
            detail_job_url = node.xpath('./div/div[1]/h3/a/@href')[0]
            if 'http' not in detail_job_url:
                detail_job_url = 'https://www.zhipin.com' + detail_job_url
            money = node.xpath('./div/div[1]/h3/a/span/text()')[0]
            addr = node.xpath('./div/div[1]/p/text()')[0]
            addr, experience, education = addr.split(',')

            company = node.xpath('./div/div[2]/div/h3/a/text()')[0]
            company_url = node.xpath('./div/div[2]/div/h3/a/@href')[0]
            if 'http' not in company_url:
                company_url = 'https://www.zhipin.com' + company_url

            company_detail = node.xpath('./div/div[2]/div/p/text()')[0]
            if company_detail.count(',') > 1:
                sectors, finance, peo_num = company_detail.split(',')
            else:
                sectors, peo_num = company_detail.split(',')
                finance = ''

            employee = node.xpath('./div/div[3]/h3/text()')[0]
            employee, employee_job = employee.split(',')
            pub_time = node.xpath('./div/div[3]/p/text()')[0]

            event = {
                'job_name': job_name,  # 职业名
                'job_url': detail_job_url,  # 具体的url
                'salary_range': money,  # 薪资
                'addr': addr,  # 地址
                'experience': experience,  # 需要的经验情况
                'education': education,  # 要求的学历
                'company': company,  # 公司名字
                'company_url': company_url,  # 公司的boss 的url
                'sectors': sectors,  # 所属的行业
                'finance': finance,  # 融资情况
                'peo_num': peo_num,  # 公司的人数
                'employee': employee,  # 发布人
                'employee_job': employee_job,  # 发布人的职位
                'pub_time': pub_time  # 发布时间
            }

            events.append(event)

        return events


if __name__ == '__main__':

    params = {
        "job_name": "golang",
        "region": "广州",
        "time_scale": 0,
        "page": 1
    }
    f = boss_spider(params)
    print(next(f))
