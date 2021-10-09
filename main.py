#!/usr/bin/env python
# -*- coding: utf-8 -*-
# main.py - 2021/10/8
#
import asyncio
import platform
import time

from loguru import logger

from spiders.async_spider import start_spider

if platform.system() == 'Windows':
    pass
else:
    try:
        import uvloop

        uvloop.install()
    except ImportError:
        logger.debug('Try install uvloop to replace the default loop.')

if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_spider())
    end = time.time()
    logger.info(f'Task finished, take {(end - start):.3f} seconds.')
