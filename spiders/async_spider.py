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

from settings import MAX_PAGE, URL, HEADERS, IMAGE_URL, IMAGE_SIZE, IMAGE_DIR
from utils import makedir

task = []


async def download_image(session, image_id, image_date):
    makedir(os.path.join(IMAGE_DIR, image_date))
    async with session.get(f'{IMAGE_URL}{image_id}_{IMAGE_SIZE}.jpg') as response:
        async with aiofiles.open(os.path.join(IMAGE_DIR, image_date, image_id + '.jpg'), 'wb') as img:
            await img.write(await response.content.read())
            logger.success(f'download image {image_id}.jpg')


async def start_spider():
    page_session = aiohttp.ClientSession()
    image_session = aiohttp.ClientSession()
    makedir(IMAGE_DIR, clean=True)

    for page in range(1, MAX_PAGE + 1):

        async with page_session.get(f'{URL}/?p={page}', headers=HEADERS) as resp:
            logger.info(f'{resp.url} status: {resp.status}')
            selector = Selector(await resp.text())
            image_list = selector.xpath("//div[@class='card progressive']")

            for image in image_list:
                image_id = image.xpath('a/@href').get()
                image_id = re.match(r'/photo/(.*?)\?force=home_*', image_id).group(1)
                image_date = image.xpath("div[@class='description']/p[@class='calendar']/em/text()").get()
                image_date = re.match(r'(\d{4}-\d{2})-\d{2}', image_date).group(1)
                logger.info(f'image name: {image_id}, date: {image_date}')
                task.append(asyncio.create_task(download_image(image_session, image_id, image_date)))

    await asyncio.wait(task)

    await page_session.close()
    await image_session.close()
