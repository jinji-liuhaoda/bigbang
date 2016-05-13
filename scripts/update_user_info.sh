#!/bin/bash

echo date
source /home/jinji/envs/zhihuibao/bin/activate
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=/home/jinji/workspace/zhihuibao/web/zhihuibao:/home/jinji/workspace/zhihuibao/web:/home/jinji/workspace/zhihuibao
python /home/jinji/workspace/zhihuibao/scripts/update_user_info.py
echo date, 'done'
