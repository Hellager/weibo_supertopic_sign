#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_form_sign_list.py
根据参数生成实际超话签到列表
"""
import json
import os
import config


def test_form_sign_list():
    configuration = config.Config()

    if os.path.exists('./data/handled_follow_list.json'):
        with open('./data/handled_follow_list.json', 'r', encoding='utf8') as f:
            row_list = json.load(f)

            print('已读取处理完成签到列表，开始筛选匹配')
            sign_list = []
            if configuration.IS_SORT == 'INCREASE':
                row_list.sort(key=lambda level: level['sort_level'])
            elif configuration.IS_SORT == 'DECREASE':
                row_list.sort(key=lambda level: level['sort_level'], reverse=True)

            if configuration.SIGN_TYPE == 'DEFAULT':
                sign_list = row_list
            else:
                for index, value in enumerate(row_list):
                    if configuration.SIGN_TYPE == 'ONLY':
                        if value['title_sub'] in configuration.SIGN_LIST:
                            sign_list.append(row_list[index])
                    elif configuration.SIGN_TYPE == 'EXCEPT':
                        if value['title_sub'] not in configuration.SIGN_LIST:
                            sign_list.append(row_list[index])

            print('已生成实际将要签到列表')
            with open('./data/sign_list.json', 'w+', encoding='utf8') as sf:
                json.dump(sign_list, sf, indent=4, ensure_ascii=False)
    else:
        print('原始超话列表文件未生成')
