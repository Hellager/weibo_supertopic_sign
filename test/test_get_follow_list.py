#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_get_follow_list.py
获取原始超话列表并写入文件 同时记录请求参数
"""
import json
import requests
import random
import time
from utils import log


def test_get_follow_list(cookie):
    headers = {
        'Accept': '*/*',
        'Host': 'api.weibo.cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
        'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    }

    page = '1'
    since_id = ''

    follow_list = []

    data = {
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
        return follow_list

    for index, value in enumerate(cookie.split('&')):
        data[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

    log.info('已生成网络请求参数')
    with open('./data/request_params.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    url = 'https://api.weibo.cn/2/cardlist'

    ## 这段测试将记录 cookie 对应账号下所有超话，仅用于检查，不建议使用
    # while True:
    #     time.sleep(random.randint(5, 10))
    #     data['v_f'] = page
    #     data['since_id'] = since_id
    #
    #     response = requests.get(url, params=data, headers=headers)
    #
    #     try:
    #         if response.json().get('errno') == -100:
    #             log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
    #             with open('./data/error_info.json', 'a+', encoding='utf-8') as f:
    #                 json.dump(response.json(), f, indent=4, ensure_ascii=False)
    #             break
    #         elif response.json().get('errno') == -200:
    #             log.error('校验参数不存在')
    #             with open('./data/error_info.json', 'a+', encoding='utf-8') as f:
    #                 json.dump(response.json(), f, indent=4, ensure_ascii=False)
    #             break
    #     except AttributeError:
    #         log.debug('success fetch data')
    #
    #     log.info('已获得原始超话列表数据，开始提取处理')
    #     with open('./data/row_follow_list.json', 'a+', encoding='utf-8') as f:
    #         json.dump(response.json(), f, indent=4, ensure_ascii=False)
    #
    #     card_group = response.json().get('cards', [{}])[0].get('card_group', [])
    #     cardlistInfo = response.json().get('cardlistInfo', [{}])
    #
    #     since_id = str(cardlistInfo["since_id"])
    #     try:
    #         page = str(json.loads(cardlistInfo["since_id"])["page"])
    #     except Exception:
    #         page = str(int(page) + 1)
    #
    #     errcode = response.json().get('errno')
    #     if errcode:
    #         log.info("page " + str(int(page) - 1) + " get data failed")
    #     else:
    #         log.info("page " + str(int(page) - 1) + " get data success")
    #
    #     for value in card_group:
    #         if value["card_type"] == "8":
    #             follow_list.append({
    #                 'title_sub': value["title_sub"],
    #                 'title_level': value["desc1"][value["desc1"].find("LV"): len(value["desc1"])],
    #                 'sort_level': int(value["desc1"][value["desc1"].find(".") + 1: len(value["desc1"])]),
    #                 'sign_status': value["buttons"][0]["name"],
    #                 'sign_action': value["buttons"][0]["params"]["action"] if value["buttons"][0][
    #                                                                               "name"] == '签到' else '',
    #                 'since_id': since_id,
    #                 'page': value["itemid"][
    #                         value["itemid"].find("super_follow") + len("super_follow") + 1: value["itemid"].find(
    #                             "super_follow") + len("super_follow") + 2]
    #             })
    #
    #      log.info(f"已处理完成原始超话列表第 {data['v_f']} 页数据")
    #     with open('./data/handled_follow_list.json', 'a+', encoding='utf-8') as f:
    #         json.dump(follow_list, f, indent=4, ensure_ascii=False)
    #
    #     if since_id == '':
    #         log.info("page " + page + " get data success")
    #         break

    # 这段测试将记录 cookie 对应账号下第一页超话，用于检查后续测试
    time.sleep(random.randint(5, 10))
    data['v_f'] = page
    data['since_id'] = since_id

    response = requests.get(url, params=data, headers=headers)

    try:
        if response.json().get('errno') == -100:
            log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
            with open('./data/error_info.json', 'a+', encoding='utf-8') as f:
                json.dump(response.json(), f, indent=4, ensure_ascii=False)
            return
        elif response.json().get('errno') == -200:
            log.error('校验参数不存在')
            with open('./data/error_info.json', 'a+', encoding='utf-8') as f:
                json.dump(response.json(), f, indent=4, ensure_ascii=False)
            return
    except AttributeError:
        log.debug('success fetch data')

    log.info('已获得原始超话列表数据，开始提取处理')
    with open('./data/row_follow_list.json', 'a+', encoding='utf-8') as f:
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
        log.info("page " + str(int(page) - 1) + " get data failed")
    else:
        log.info("page " + str(int(page) - 1) + " get data success")

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

    log.info(f"已处理完成原始超话列表第 {data['v_f']} 页数据")
    with open('./data/handled_follow_list.json', 'a+', encoding='utf-8') as f:
        json.dump(follow_list, f, indent=4, ensure_ascii=False)

    if since_id == '':
        log.info("page " + page + " get data success")
        return
