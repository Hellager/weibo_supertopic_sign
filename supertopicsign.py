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
        self.current_signed_count = 0
        self.user_cookie_dict = {}
        self.user_topic_list = {}

        self.errmsg = ''
        self.request_headers = {
            'Accept': '*/*',
            'Host': 'api.weibo.cn',
            'User-Agent': 'WeiboOverseas/4.4.1 (iPhone; iOS 14.7.1; Scale/3.00)',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
        }
        self.notifier = notifier.Notifier()

    @staticmethod
    def get_username(cookie):
        log.info('Start get username')
        username = ""
        request_username_headers = {
            'Accept': '*/*',
            'Host': 'api.weibo.cn',
            'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
            'User-Agent': 'WeiboOverseas/4.7.8 (iPhone; iOS 15.5; Scale/3.00)',
            'Content-type': 'application/x-www-form-urlencoded',
        }

        request_username_url = 'https://api.weibo.cn/2/users/update'

        response = requests.post(request_username_url, params=cookie, headers=request_username_headers)

        try:
            username = response.json().get('name')
        except AttributeError:
            log.error('Failed to get username for current user')

        # if username == "":
        #     param_from_start_pos = cookie.find('from') + len('from=')
        #     username = cookie[param_from_start_pos:param_from_start_pos + 10]

        return username

    def form_user_cookie_dict(self):
        log.info('Start forming user cookie dict')
        row_user_url = self.config.ROW_URL.split(';')
        for index, url in enumerate(row_user_url):
            time.sleep(random.randint(3, 5))
            cookie_start_pos = 0
            if 'cardlist?' in url:
                cookie_start_pos = url.find('cardlist?') + len('cardlist?')
            elif 'aid' in url:
                cookie_start_pos = url.find('aid')
            else:
                break  # cookie invalid

            user_cookie = url[cookie_start_pos:]
            user_name = self.get_username(user_cookie)
            if user_name == "":
                user_name = "user_" + str(index)

            self.user_cookie_dict[user_name] = user_cookie

    @staticmethod
    def is_user_all_topic_signed(topic_list):
        for topic in topic_list:
            if topic['sign_status'] != "已签":
                return False

        return True

    def is_all_user_signed(self):
        for user, signed_list in self.user_topic_list.items():
            if not self.is_user_all_topic_signed(signed_list):
                return False

        return True

    def update_user_topic_list(self, username, topic_list):
        self.user_topic_list[username] = topic_list

    @staticmethod
    def form_params(cookie):
        log.info('Start forming requests params')

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

        if cookie == '':
            return row_params

        for index, value in enumerate(cookie.split('&')):
            row_params[value[0: value.find('=')]] = value[value.find('=') + 1: len(value)]

        return row_params

    def get_follow_list(self, username):
        log.info('Start getting super topic follow list')

        page = '1'
        since_id = ''

        follow_list = []

        user_cookie = self.user_cookie_dict[username]
        data = self.form_params(user_cookie)

        url = 'https://api.weibo.cn/2/cardlist'

        while True:
            time.sleep(random.randint(5, 10))
            data['v_f'] = page
            data['since_id'] = since_id

            response = requests.get(url, params=data, headers=self.request_headers)

            try:
                if response.json().get('errno') == -100:
                    self.errmsg = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取'
                    log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
                    break
                elif response.json().get('errno') == -200:
                    self.errmsg = '校验参数不存在'
                    log.error('校验参数不存在')
                    break
            except AttributeError:
                log.debug('success fetch data')

            card_group = response.json().get('cards', [{}])[0].get('card_group', [])
            cardlistInfo = response.json().get('cardlistInfo', [{}])

            since_id = str(cardlistInfo["since_id"])
            try:
                page = str(json.loads(cardlistInfo["since_id"])["page"])
            except Exception:
                page = str(int(page) + 1)

            errcode = response.json().get('errno')
            if errcode:
                log.info("page " + str(int(page)-1) + " get data failed")
            else:
                log.info("page " + str(int(page)-1) + " get data success")

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
                log.info("page " + page + " get data success")
                break

        return follow_list

    def form_sign_list(self, row_list):
        log.info('Start forming super topic sign list')

        if self.config.IS_SORT == 'INCREASE':
            row_list.sort(key=lambda level: level['sort_level'])
        elif self.config.IS_SORT == 'DECREASE':
            row_list.sort(key=lambda level: level['sort_level'], reverse=True)

        return row_list

    def do_sign(self, cookie, to_sign_list):
        base_url = 'https://api.weibo.cn'
        sign_data = self.form_params(cookie)

        log.info('Start doing sign tasks')

        for index, value in enumerate(to_sign_list):
            if self.current_signed_count >= self.config.SIGN_ONCE_COUNT:
                break

            page = value['page']
            since_id = value['since_id']

            sign_data['v_f'] = f'{page}'
            sign_data['since_id'] = f'{since_id}'

            if value['sign_status'] == '签到':
                time.sleep(random.randint(15, 30))
                sign_url = base_url + value['sign_action']
                response = requests.post(sign_url, headers=self.request_headers, data=sign_data)

                self.current_signed_count += 1

                if response.json().get('msg') == '已签到':
                    log.info('超话 ' + value["title_sub"] + ' 签到成功 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

                if response.json().get('errno') == -100:
                    self.errmsg = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取'
                    log.error('由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取')
                    break
                else:
                    if response.json().get('msg') == '已签到':
                        value['sign_status'] = '已签'
            elif value['sign_status'] == '已签':
                log.info('超话 ' + value["title_sub"] + ' 已签到 ' + str(int(index) + 1) + '/' + str(len(to_sign_list)))

        return to_sign_list
