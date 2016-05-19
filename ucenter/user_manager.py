# coding: utf-8

import requests
from .base_manager import BaseManager
from .constants import GET, POST
from .models import Cuser

WX_USER_INFO_URL = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN'


class UserManager(BaseManager):

    instance = None

    def __init__(self):
        super(UserManager, self).__init__()

    @staticmethod
    def get_instance():
        if UserManager.instance is None:
            UserManager.instance = UserManager()

        return UserManager.instance

    def update_wechat_user_info(self, openid):
        # 获得openid和access_token
        access_token = self.get_token()
        obj = self.wx_request(POST, WX_USER_INFO_URL.format(
            access_token,
            openid,
        ))

        name = obj.get('nickname', '')
        city = obj.get('city', '')
        province = obj.get('province', '')
        country = obj.get('country', '')
        headimgurl = obj.get('headimgurl', '')
        # 同步用户微信头像
        Cuser.objects.filter(openid=openid).update(headimgurl=headimgurl, name=name, city=city, province=province, country=country)
        return True


user_manager = UserManager.get_instance()
