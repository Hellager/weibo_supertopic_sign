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


def test_do_sign_tasks():
    configuration = config.Config()
    base_url = 'https://api.weibo.cn'
    headers = {
        'Accept': '*/*',
        'Host': 'api.weibo.cn',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'X-Sessionid': '14E2F408-1B5D-4A0E-BA8A-758D162AD79A',
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
    if configuration.ROW_URL == '':
        return sign_params

    row_text = configuration.ROW_URL[
               configuration.ROW_URL.find('cardlist?') + len('cardlist?'):len(configuration.ROW_URL)]
    for index, value in enumerate(row_text.split('&')):
        sign_params[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

    if os.path.exists('./data/handled_follow_list.json'):
        with open('./data/handled_follow_list.json', 'r', encoding='utf8') as f:
            to_sign_list = json.load(f)

        start_time = time.clock()
        print('已读取签到列表，开始执行签到操作')
        for index, value in enumerate(to_sign_list):
            page = value['page']
            since_id = value['since_id']

            sign_params['v_f'] = f'{page}'
            sign_params['since_id'] = f'{since_id}'

            time.sleep(random.randint(15, 30))

            if value['sign_status'] == '签到':
                sign_url = base_url + value['sign_action']
                response = requests.post(sign_url, headers=headers, data=sign_params)

                if response.json().get('msg') == '已签到':
                    print('超话 ' + value["title_sub"] + ' 签到成功 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

                if response.json().get('errno') == -100:
                    print('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
                    break
                else:
                    if response.json().get('msg') == '已签到':
                        value['sign_status'] = '已签'
            elif value['sign_status'] == '已签':
                print('超话 ' + value["title_sub"] + ' 已签到 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

        end_time = time.clock()
        print('完成全部签到任务')
        print('签到耗时: %s Seconds' % round(end_time-start_time, 2))
        with open('./data/sign_result.json', 'w+', encoding='utf8') as f:
            json.dump(to_sign_list, f, indent=4, ensure_ascii=False)
