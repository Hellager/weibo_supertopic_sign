#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_index.py
执行测试
"""
from test_get_follow_list import *
from test_form_sign_list import *
from test_do_sign_tasks import *

username = ""
user_cookie = ""

test_get_follow_list(user_cookie)
test_form_sign_list()
test_do_sign_tasks()
