# coding: utf-8

import os

QINIU_DOMAIN = 'o79kbc454.bkt.clouddn.com'
ACCESS_KEY = 'ht7VHWxYJGzO4fZYpvAZuXnk3nVvXftnVtSM8y6f'
SECRET_KEY = 'h8CXcT5V3vlc_7LyvzCsMl2Uz4fFhal5RfROxDlJ'
BUCKET_NAME = 'temple'


def upload(prefix, key, localpath):

    from qiniu import Auth, put_file
    q = Auth(ACCESS_KEY, SECRET_KEY)

    key = os.path.join(prefix, key)
    token = q.upload_token(BUCKET_NAME, key)
    ret, info = put_file(token, key, localpath)


def url(prefix, key):
    return 'http://' + os.path.join(QINIU_DOMAIN, prefix, key)


def get_extension(filename):
    arr = filename.split('.')
    if not arr:
        return ''

    return arr[-1]


def handle_uploaded_file(f, path):
    from settings import UPLOAD_DIR
    with open(os.path.join(UPLOAD_DIR, path), 'wb') as dest:
        for chunk in f.chunks():
            dest.write(chunk)