# coding: utf-8

import urllib
from settings import DOMAIN

GET = 'GET'
POST = 'POST'

WX_APP_ID = 'wx898df5f036249412'
WX_SECRET = '060043bb37e2fa3a38ec573e7239ff4b'
WX_MCH_ID = '1337862001'

USE_FAKE_WECHAT_USER = False

WX_REDIRECT_URI = '{}/cuser/wechat_do_login/'.format(DOMAIN,)
WX_GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'
WX_AUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'.format(
    WX_APP_ID,
    urllib.quote_plus(WX_REDIRECT_URI)
)
