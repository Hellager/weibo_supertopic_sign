#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_follow_list.py
获取原始超话列表并写入文件 同时记录请求参数
"""
import json
import requests
import config


def test_get_follow_list():
    configuration = config.Config()
    headers = {
        'Accept': '*/*',
        'Host': 'api.weibo.cn',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        'X-Sessionid': '14E2F408-1B5D-4A0E-BA8A-758D162AD79A',
    }

    page = '1'
    since_id = ''

    follow_list = []

    row_params = {
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
        return row_params

    row_text = configuration.ROW_URL[
               configuration.ROW_URL.find('cardlist?') + len('cardlist?'):len(configuration.ROW_URL)]
    for index, value in enumerate(row_text.split('&')):
        row_params[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

    print('已生成网络请求参数')
    with open('./data/request_params.json', 'w+', encoding='utf-8') as f:
        json.dump(row_params, f, indent=4, ensure_ascii=False)

    url = 'https://api.weibo.cn/2/cardlist'

    row_params['v_f'] = page
    row_params['since_id'] = since_id

    response = requests.get(url, params=row_params, headers=headers)

    if response.json().get('errno') == -100:
        print('验证错误')
        with open('./data/error_info.json', 'w+', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return
    elif response.json().get('errno') == -200:
        print('校验参数错误')
        with open('./data/error_info.json', 'w+', encoding='utf-8') as f:
            json.dump(response.json(), f, indent=4, ensure_ascii=False)
        return

    print('已获得原始超话列表数据，开始提取处理')
    with open('./data/row_follow_list.json', 'w+', encoding='utf-8') as f:
        json.dump(response.json(), f, indent=4, ensure_ascii=False)

    card_group = response.json().get('cards', [{}])[0].get('card_group', [])
    cardlistInfo = response.json().get('cardlistInfo', [{}])

    since_id = str(cardlistInfo["since_id"])
    try:
        page = str(json.loads(cardlistInfo["since_id"])["page"])
    except Exception:
        page = str(int(page) + 1)

    errcode = response.json().get('errno')
    if errcode:
        print("page " + str(int(page) - 1) + " get data failed")
    else:
        print("page " + str(int(page) - 1) + " get data success")

    for value in card_group:
        if value["card_type"] == "8":
            follow_list.append({
                'title_sub': value["title_sub"],
                'title_level': value["desc1"][value["desc1"].find("LV"): len(value["desc1"])],
                'sort_level': int(value["desc1"][value["desc1"].find(".") + 1: len(value["desc1"])]),
                'sign_status': value["buttons"][0]["name"],
                'sign_action': value["buttons"][0]["params"]["action"] if value["buttons"][0][
                                                                              "name"] == '签到' else '',
                'since_id': since_id,
                'page': value["itemid"][
                        value["itemid"].find("super_follow") + len("super_follow") + 1: value["itemid"].find(
                            "super_follow") + len("super_follow") + 2]
            })

    print('已处理完成原始超话列表数据')
    with open('./data/handled_follow_list.json', 'w+', encoding='utf-8') as f:
        json.dump(follow_list, f, indent=4, ensure_ascii=False)
