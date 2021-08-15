# -*- coding: utf-8 -*-
import re
import getpass

import mysql.connector
import asyncio
from xpinyin import Pinyin

from blivedm.blivedm import BLiveClient, SuperChatMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'kitzuki'
room_id = VtuberOfInterest[selected_vtuber]

mysqlHost = '172.17.0.4'
mysqlUsername = 'root'
mysqlPassword = ''

gift_threshold = 0
filename = 'log.txt'
pinyin = Pinyin()

def inputMysqlPassword():
    global mysqlPassword
    mysqlPassword = getpass.getpass(prompt='MySQL Password: ')

def parseMessage(message: SuperChatMessage):
    uname = message.uname
    uname_pinyin = re.sub("-", " ", pinyin.get_pinyin(message.uname, tone_marks='marks'))
    uid = message.uid
    content = message.message
    price = message.price
    return uname, uname_pinyin, uid, content, price

def writeMySQL(val):
    mydb = mysql.connector.connect(
        host=mysqlHost,
        user=mysqlUsername,
        password=mysqlPassword,
        database=selected_vtuber
    )
    mycursor = mydb.cursor()

    sql = "INSERT INTO superchats (uname, pinyin, uid, message, price) VALUES (%s, %s, %s, %s, %s)"

    mycursor.execute(sql, val)
    mydb.commit()

class MyBLiveClient(BLiveClient):
    async def _on_super_chat(self, message: SuperChatMessage):
        val = parseMessage(message)
        writeMySQL(val)

async def main():
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()

if __name__ == '__main__':
    inputMysqlPassword()
    asyncio.get_event_loop().run_until_complete(main())
