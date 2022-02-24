#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
config.py
从本地config.json中获取参数变量
"""
import json
import os
import sys
from utils import log


class Config(object):
    """
    Get configuration from the config.json file or from the environment.
    Note:
          ROW_URL: This is the row url from the network package,
                    which should include field gsid, aid, from, s
          SIGN_TYPE: This is the variable to choose the sign method(DEFAULT, ONLY, EXCEPT)
                      DEFAULT -> This will sign all your superindex
                      ONLY -> This will sign the superindex only in your SIGN_LIST
                      EXCEPT -> This will sign the superindex only not in your SIGN_LIST
          SIGN_LIST: This is the sign list
          Ding_SECRET: This is the secret key of your ding ding bot
          Ding_WEBHOOK: This is the webhook of your ding ding bot
          Server_KEY: This is the key of your server chan
          QMsg_KEY: This is the key of your qmsg chan
          IS_SORT: This is the variable to choose whether the result will be sorted to display or not
                    INCREASE -> The results will be displayed incrementally according to the level
                    DECREASE -> The results will be displayed in descending order according to the level
          DISP_TYPE: This is the variable to choose your result display type
                     The result of failed check-in will always be displayed in detail
                       DEFAULT -> The result of successful check-in will be omitted
                       DETAIL -> The result of successful check-in will be displayed in detail
    """

    def __init__(self):
        project_path = os.path.dirname(__file__)
        config_file = os.path.join(project_path, 'config.json')
        if not os.path.exists(config_file):
            log.error('Please check your config.json, it seems not to be exisiting')
            sys.exit()

        with open(config_file, 'r', encoding='utf-8') as fl_obj:
            self.config_json = json.load(fl_obj)

        self.ROW_URL = self.get_config('ROW_URL')
        self.SIGN_TYPE = self.get_config('SIGN_TYPE')
        self.SIGN_LIST = self.get_config('SIGN_LIST')
        self.Ding_SECRET = self.get_config('DING_SECRET')
        self.Ding_WEBHOOK = self.get_config('DING_WEBHOOK')
        self.Server_KEY = self.get_config('SERVER_KEY')
        self.QMsg_KEY = self.get_config('QMSG_KEY')
        self.IS_SORT = self.get_config('IS_SORT')
        self.DISP_TYPE = self.get_config('DISP_TYPE')

    def get_config(self, name: str):
        if os.environ.get(name):
            value = os.environ[name]
        else:
            value = self.config_json.get(name, '')

        return value
