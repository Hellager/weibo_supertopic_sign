import json
import requests
import datetime
import time
import hmac
import hashlib
import base64
import urllib.parse
import sys
sys.path.append("..")
import config
from utils import log


class DingBot(object):
    def __init__(self):
        self.secret = config.config.Ding_SECRET
        self.webhook = config.config.Ding_WEBHOOK

    @staticmethod
    def form_content(user_signed_list, style):
        log.info('Starting forming ding ding bot content')

        text = "### --------微博超话签到-------- \n"
        week_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        tip_time = datetime.datetime.now().strftime('%m-%d')
        days = week_list[datetime.datetime.now().weekday()]

        content = text + tip_time + ' ' + days + '\n\n'

        for username, signed_list in user_signed_list.items():
            user_content = ""
            success_count = 0
            fail_list = []
            for value in signed_list:
                if value["sign_status"] == "已签":
                    success_count = success_count + 1
                elif value["sign_status"] == "签到":
                    fail_list.append(value["title_sub"])

            if style == 'DEFAULT':
                user_content = '用户 ' + username + '\n\n - 成功签到 ' + str(
                    success_count) + ' / ' + str(len(signed_list))
            elif style == 'DETAIL':
                user_content = '用户 ' + username + '\n\n成功签到 \n\n'
                for value in signed_list:
                    user_content = user_content + '- ' + value['title_level'] + ' ' + value['title_sub'] + '  ✅ \n'

            if len(fail_list) != 0:
                user_content = user_content + '\n\n签到失败 \n\n'
            for value in fail_list:
                user_content = user_content + '- ' + str(value) + '  ❌ \n'

            content += user_content

        return content

    def send(self, content, err):
        log.info('Starting sending ding ding bot message')

        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        url = '%s&timestamp=%s&sign=%s' % (self.webhook, timestamp, sign)

        if err != '':
            content = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取微博超话签到相关参数'

        headers = {'Content-Type': 'application/json'}
        data = {
            "msgtype": "markdown",
            'markdown': {
                'title': '微博超话签到',
                'text': f'{content}\n'
            }
        }

        res = requests.post(url, data=json.dumps(data), headers=headers)

        if res.json()['errmsg'] == 'ok':
            log.info('Ding ding bot message send success')
