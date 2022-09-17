import json
import requests
import datetime
import config
import sys
sys.path.append("..")
import config
from utils import log

class ServerChan(object):
    def __init__(self):
        self.key = config.config.Server_KEY

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
        log.info('Starting sending server chan message')

        if err != '':
            content = '由于你近期修改过密码，或开启了登录保护，参数失效，请重新获取微博超话签到相关参数'

        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'text': '微博超话签到通知',
            'desp': f'{content}'
        }
        url = f"https://sctapi.ftqq.com/{self.key}.send"

        response = requests.post(url, data=data, headers=headers)

        if json.loads(response.text)["data"]['error'] == 'SUCCESS':
            log.info('Server chan message send success')
