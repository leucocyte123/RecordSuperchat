# -*- coding: utf-8 -*-
import re
import getpass

import mysql.connector
import asyncio
from xpinyin import Pinyin

from blivedm.blivedm import BLiveClient, SuperChatMessage, GiftMessage, GuardBuyMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'xuehusang'
room_id = VtuberOfInterest[selected_vtuber]

mysqlHost = '172.17.0.4'
mysqlUsername = 'root'
mysqlPassword = ''

gift_threshold = 0
pinyin = Pinyin()

def inputMysqlPassword():
    global mysqlPassword
    mysqlPassword = getpass.getpass(prompt='MySQL Password: ')

def parseMessageGift(message: GiftMessage):
    uname = message.uname
    uname_pinyin = re.sub("-", " ", pinyin.get_pinyin(message.uname, tone_marks='marks'))
    uid = message.uid
    content = "%s x %d" % (message.gift_name, message.num)
    price = int(message.total_coin / 100)
    return uname, uname_pinyin, uid, content, price

def parseMessageGuard(message: GuardBuyMessage):
    def guard_level_to_name(guard_level):
        if guard_level == 1:
            return '总督'
        elif guard_level == 2:
            return '提督'
        elif guard_level == 3:
            return '舰长'
        else:
            return '非舰队'

    uname = message.uname
    uname_pinyin = re.sub("-", " ", pinyin.get_pinyin(message.uname, tone_marks='marks'))
    uid = message.uid
    content = "%s x %d" % (guard_level_to_name(message.guard_level), message.num)
    price = int(message.price * message.num / 100)
    return uname, uname_pinyin, uid, content, price

def parseMessageSuperchat(message: SuperChatMessage):
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
    async def _on_receive_gift(self, gift: GiftMessage):
        if gift.coin_type != 'gold':
            return
        val = parseMessageGift(gift)
        writeMySQL(val)

    async def _on_buy_guard(self, guard: GuardBuyMessage):
        val = parseMessageGuard(guard)
        writeMySQL(val)

    async def _on_super_chat(self, superchat: SuperChatMessage):
        val = parseMessageSuperchat(superchat)
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
