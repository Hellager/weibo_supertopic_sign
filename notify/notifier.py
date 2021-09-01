from . import dingdingbot
from . import serverchan
from . import qmsgchan
import sys
sys.path.append("..")
import config
from utils import log


class Notifier(object):
    def __init__(self):
        self.config = config.config
        self.ding_bot = dingdingbot.DingBot()
        self.server_chan = serverchan.ServerChan()
        self.qmesg_chan = qmsgchan.QmsgChan()

    def do_notify(self, sign_list, errmsg):
        log.info('Starting notifying')
        if self.config.Ding_SECRET != '' and self.config.Ding_WEBHOOK != '':
            self.ding_bot.send(self.ding_bot.form_content(sign_list, self.config.DISP_TYPE), errmsg)

        if self.config.Server_KEY != '':
            self.server_chan.send(self.server_chan.form_content(sign_list, self.config.DISP_TYPE), errmsg)

        if self.config.QMsg_KEY != '':
            self.qmesg_chan.send(self.qmesg_chan.form_content(sign_list, self.config.DISP_TYPE), errmsg)
