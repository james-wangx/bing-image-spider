#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mysql.py - 2021/10/9
# mysql operation
import aiomysql
from loguru import logger

from settings import MYSQL_HOST, MYSQL_USER, MYSQL_PORT, MYSQL_DATABASE, MYSQL_PASSWORD, MYSQL_TABLE


class Mysql:

    async def init_mysql(self, loop, clean=False):
        """
        create a connection

        :param loop:
        :param clean: drop and create a new table
        """
        self.conn = await aiomysql.connect(host=MYSQL_HOST,
                                           port=MYSQL_PORT,
                                           user=MYSQL_USER,
                                           db=MYSQL_DATABASE,
                                           password=MYSQL_PASSWORD,
                                           loop=loop)
        self.cur = await self.conn.cursor()
        if clean:
            await self.cur.execute(f"DROP TABLE IF EXISTS {MYSQL_TABLE};")
            await self.cur.execute(f"""
                        CREATE TABLE {MYSQL_TABLE}
                        (id VARCHAR(255) NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        copyright VARCHAR(255) NOT NULL,
                        date DATE NOT NULL,
                        url VARCHAR(255) NOT NULL,
                        PRIMARY KEY(id));
            """)
            await self.conn.commit()

    async def insert_item(self, item: dict):
        keys = ','.join(item.keys())
        values = ','.join(['%s'] * len(item.values()))
        sql = f"INSERT INTO {MYSQL_TABLE} ({keys}) VALUES({values});"
        try:
            await self.cur.execute(sql, tuple(item.values()))
            await self.conn.commit()
            logger.info(f'Insert {item.items()} to {MYSQL_DATABASE}.{MYSQL_TABLE}')
        except Exception as e:
            logger.error(f"Insert item fail, {e.args}")
            await self.conn.rollback()

    async def close(self):
        await self.cur.close()
        self.conn.close()
