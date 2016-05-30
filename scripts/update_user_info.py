# coding: utf-8

import django;django.setup()
from ucenter.user_manager import user_manager
from ucenter.models import (
    Cuser,
)


def update_wechat_user_info():
    # cusers = Cuser.objects.all()
    # for cuser in cusers:
    #     if cuser.openid:
            # user_manager.update_wechat_user_info(cuser.openid)
    return True


if __name__ == '__main__':
    update_wechat_user_info()
