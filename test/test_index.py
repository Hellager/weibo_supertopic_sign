#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_index.py
执行测试

config.json 及 config.py 在当前版本并不涉及，可无视

手动设置 username 及 user_cookie 变量后即可直接运行测试

data文件夹
1. 执行完 test_get_follow_list 函数后将生成三个 json 文件
request_params.json 对应网络请求参数
row_follow_list.json 对应原始获得的超话列表参数
handled_follow_list.json 对应提取有用信息后的超话列表参数

查看 handled_follow_list.json 中检查超话参数是否正确

2. 执行完 test_form_sign_list 函数后将生成 sign_list.json 文件
将对 handled_follow_list.json 中的参数根据 config 设置进行等级排序处理

3. 执行完 test_do_sign_tasks 函数后将生成 sign_result.json 文件
将记录签到结果，与 sign_list.json 中文件对比查看效果
"""
from test_get_follow_list import *
from test_form_sign_list import *
from test_do_sign_tasks import *

username = ""
user_cookie = ""

test_get_follow_list(user_cookie)
test_form_sign_list()
test_do_sign_tasks(user_cookie)
