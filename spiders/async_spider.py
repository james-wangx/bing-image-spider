#!/usr/bin/env python
# -*- coding: utf-8 -*-
# async_spider.py - 2021/10/7
#
import asyncio
import os.path
import re

import aiofiles
import aiohttp
from loguru import logger
from parsel import Selector

from database.mysql import Mysql
from settings import MAX_PAGE, URL, HEADERS, IMAGE_URL, IMAGE_SIZE, IMAGE_DIR
from utils import makedir

task = []


async def save_to_mysql(mysql, image, image_session):
    image_id = image.xpath('a/@href').get()
    image_id = re.match(r'/photo/(.*?)\?force=home_*', image_id).group(1)
    image_date = image.xpath("div[@class='description']/p[@class='calendar']/em/text()").get()
    image_url = f'{IMAGE_URL}{image_id}_{IMAGE_SIZE}.jpg'
    image_des = image.xpath("div[@class='description']/h3/text()").get()

    try:
        image_des = re.match(r'(.*?)\s?[(（]\s?©\s?(.*?)\s?[）)]', image_des)
        image_name = image_des.group(1)
        image_copyright = image_des.group(2)
        item = {
            'id': image_id,
            'name': image_name,
            'copyright': image_copyright,
            'date': image_date,
            'url': image_url
        }
        await mysql.insert_item(item)
        task.append(asyncio.create_task(download_image(image_session, image_id, image_name, image_date[:-3])))
    except AttributeError as e:
        logger.error(f"{e.args}, image date is {image_date}.")


async def download_image(session, image_id, image_name, image_date):
    makedir(os.path.join(IMAGE_DIR, image_date))
    async with session.get(f'{IMAGE_URL}{image_id}_{IMAGE_SIZE}.jpg') as response:
        async with aiofiles.open(os.path.join(IMAGE_DIR, image_date, image_name + '.jpg'), 'wb') as img:
            await img.write(await response.content.read())
            logger.info(f'Download image {image_name}.jpg')


async def start_spider(loop):
    page_session = aiohttp.ClientSession()
    image_session = aiohttp.ClientSession()
    makedir(IMAGE_DIR, clean=True)
    mysql = Mysql()
    await mysql.init_mysql(loop, clean=True)

    for page in range(1, MAX_PAGE + 1):
        async with page_session.get(f'{URL}/?p={page}', headers=HEADERS) as resp:
            logger.info(f'Fetch url {resp.url}, status: {resp.status}')
            selector = Selector(await resp.text())
            image_list = selector.xpath("//div[@class='card progressive']")
            for image in image_list:
                await save_to_mysql(mysql, image, image_session)

    await asyncio.wait(task)

    await mysql.close()
    await image_session.close()
    await page_session.close()
