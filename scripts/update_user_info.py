# coding: utf-8

import django;django.setup()
from ucenter.user_manager import user_manager
from ucenter.models import (
    User,
)


def update_wechat_user_info():
    users = User.objects.all()
    for user in users:
            if user.openid:
                user_manager.update_wechat_user_info(user.openid)


if __name__ == '__main__':
    update_wechat_user_info()
