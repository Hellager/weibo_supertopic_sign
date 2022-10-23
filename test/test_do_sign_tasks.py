#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_do_sign_tasks.py
实际完成签到操作并获得返回值
"""
import os
import json
import time
import random
import requests
import config
from utils import log


def test_do_sign_tasks(cookie):
    base_url = 'https://api.weibo.cn'
    headers = {
        'Accept': '*/*',
        'Host': 'api.weibo.cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    }

    sign_params = {
        'aid': '',
        'c': '',
        'containerid': '',
        'extparam': '',
        'from': '',
        'gsid': '',
        'i': '',
        'lang': '',
        'page': '',
        's': '',
        'ua': '',
        'v_f': '',
        'v_p': '',
        'since_id': ''
    }

    if cookie == '':
        log.error('Error: Cookie invalid')
        return sign_params

    for index, value in enumerate(cookie.split('&')):
        sign_params[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

    if os.path.exists('./data/sign_list.json'):
        with open('./data/sign_list.json', 'r', encoding='utf8') as f:
            to_sign_list = json.load(f)

        start_time = time.clock()
        log.info('已读取签到列表，开始执行签到操作')
        for index, value in enumerate(to_sign_list):
            page = value['page']
            since_id = value['since_id']

            sign_params['v_f'] = f'{page}'
            sign_params['since_id'] = f'{since_id}'

            time.sleep(random.randint(15, 30))

            if value['sign_status'] == '签到':
                time.sleep(random.randint(15, 30))
                sign_url = base_url + value['sign_action']
                response = requests.post(sign_url, headers=headers, data=sign_params)

                # current_signed_count += 1

                if response.json().get('msg') == '已签到':
                    log.info('超话 ' + value["title_sub"] + ' 签到成功 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

                if response.json().get('errno') == -100:
                    log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
                    break
                else:
                    if response.json().get('msg') == '已签到':
                        value['sign_status'] = '已签'
            elif value['sign_status'] == '已签':
                log.info('超话 ' + value["title_sub"] + ' 已签到 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

        end_time = time.clock()
        print('完成全部签到任务')
        print('签到耗时: %s Seconds' % round(end_time-start_time, 2))
        with open('./data/sign_result.json', 'w+', encoding='utf8') as f:
            json.dump(to_sign_list, f, indent=4, ensure_ascii=False)
