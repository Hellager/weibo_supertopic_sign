import config
import json
import random
import time
import requests
from utils import log
from notify import notifier


class SuperTopicHandler(object):
    def __init__(self):
        self.config = config.config
        self.errmsg = ''
        self.headers = {
            'Accept': '*/*',
            'Host': 'api.weibo.cn',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'X-Sessionid': '14E2F408-1B5D-4A0E-BA8A-758D162AD79A',
        }
        self.notifier = notifier.Notifier()

    def form_params(self):
        log.info('Starting forming requests params')

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

        if self.config.ROW_URL == '':
            return row_params

        row_text = self.config.ROW_URL[
                   self.config.ROW_URL.find('cardlist?') + len('cardlist?'):len(self.config.ROW_URL)]
        for value in enumerate(row_text.split('&')):
            row_params[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

        return row_params

    def get_follow_list(self):
        log.info('Starting getting super topic follow list')

        page = '1'
        since_id = ''

        follow_list = []

        data = self.form_params()

        url = 'https://api.weibo.cn/2/cardlist'

        while True:
            time.sleep(random.randint(3, 5))
            data['v_f'] = page
            data['since_id'] = since_id

            response = requests.get(url, params=data, headers=self.headers)

            if response.json().get('errno') == -100:
                self.errmsg = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取'
                log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
                break
            elif response.json().get('errno') == -200:
                self.errmsg = '校验参数不存在'
                log.error('校验参数不存在')
                break

            card_group = response.json().get('cards', [{}])[0].get('card_group', [])
            cardlistInfo = response.json().get('cardlistInfo', [{}])

            since_id = str(cardlistInfo["since_id"]);
            try:
                page = str(json.loads(cardlistInfo["since_id"])["page"]);
            except Exception:
                page = '8'

            errcode = response.json().get('errno')
            if errcode:
                log.info("page " + page + " get data failed")
            else:
                log.info("page " + page + " get data success")

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

            if since_id == '':
                break

        return follow_list

    def form_sign_list(self, row_list):
        log.info('Starting forming super topic sign list')

        sign_list = []
        if self.config.IS_SORT == 'INCREASE':
            row_list.sort(key=lambda level: level['sort_level'])
        elif self.config.IS_SORT == 'DECREASE':
            row_list.sort(key=lambda level: level['sort_level'], reverse=True)

        if self.config.SIGN_TYPE == 'DEFAULT':
            sign_list = row_list
        else:
            for index, value in enumerate(row_list):
                if self.config.SIGN_TYPE == 'ONLY':
                    if value['title_sub'] in self.config.SIGN_LIST:
                        sign_list.append(row_list[index])
                elif self.config.SIGN_TYPE == 'EXCEPT':
                    if value['title_sub'] not in self.config.SIGN_LIST:
                        sign_list.append(row_list[index])

        return sign_list

    def do_sign(self, to_sign_list):
        log.info('Starting doing sign tasks')

        base_url = 'https://api.weibo.cn'

        for value in enumerate(to_sign_list):
            page = value['page']
            since_id = value['since_id']

            data = {
                'aid': '01A-y_MsMUYarhUt6_xHUeAE3kC84H9oKkBMWh7Op-87-U6v4.',
                'c': 'weicoabroad',
                'containerid': '100803_-_followsuper',
                'extparam': '',
                'from': '1244193010',
                'gsid': '_2A25MIpzfDeRxGeRI6lUS9ifOzz6IHXVteZcXrDV6PUJbkdCOLWXYkWpNUwauaVSGovz2eC14k8oWt5rLnz-QnC8h',
                'i': '6050a0f',
                'lang': 'zh_CN',
                'page': '1',
                's': '2625458f',
                'ua': 'iPhone13,2_iOS14.7.1_Weibo_intl._4410_wifi',
                'v_f': f'{page}',
                'v_p': '59',
                'since_id': f'{since_id}'
            }

            time.sleep(random.randint(0, 5))

            if value['sign_status'] == '签到':
                sign_url = base_url + value['sign_action']
                response = requests.post(sign_url, headers=self.headers, data=data)

                if response.get('msg') == '已签到':
                    value['sign_status'] = '已签'

        self.notifier.do_notify(to_sign_list, self.errmsg)
