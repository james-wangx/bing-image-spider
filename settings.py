#!/usr/bin/env python
# -*- coding: utf-8 -*-
# settings.py - 2021/10/7
# project settings
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

MAX_PAGE = 73
IMAGE_SIZE = 'UHD'
IMAGE_URL = 'https://www.bing.com/th?id=OHR.'
IMAGE_DIR = 'images'

URL = 'https://bing.ioliu.cn'
HEADERS = {
    'Host': 'bing.ioliu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 Safari/537.36',
}

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_TABLE = 'test'
MYSQL_DATABASE = 'spiders'
MYSQL_PASSWORD = 'mysql'
