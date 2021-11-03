#!/usr/bin/env python
# -*- coding: utf-8 -*-
# settings.py - 2021/10/7
# project settings
import argparse
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

MAX_PAGE = 75
IMAGE_SIZE = 'UHD'
IMAGE_URL = 'https://www.bing.com/th?id=OHR.'
IMAGE_DIR = 'images'

OFFICIAL_API = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-cn'

URL = 'https://bing.ioliu.cn'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/92.0.4515.131 Safari/537.36',
}

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_TABLE = os.getenv('MYSQL_TABLE', 'bing_images')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'spiders')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'mysql666')

parser = argparse.ArgumentParser(description="Bing Image Spider")
parser.add_argument('--daily', type=int, default=1,
                    help='Daily update or not.')
args = parser.parse_args()
DAILY_UPDATE = args.daily

if DAILY_UPDATE:
    DIR_CLEAN = False
    TABLE_CLEAN = False
else:
    DIR_CLEAN = True
    TABLE_CLEAN = True
