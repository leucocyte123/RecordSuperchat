# -*- coding: utf-8 -*-
import re
import logging
from datetime import datetime

import asyncio
from xpinyin import Pinyin

from blivedm.blivedm import BLiveClient, GiftMessage, GuardBuyMessage, SuperChatMessage, DanmakuMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'kitzuki'
room_id = VtuberOfInterest[selected_vtuber]

gift_threshold = 0
filename = 'log.txt'
pinyin_data_path = 'Mandarin.dat'
pinyin = Pinyin(pinyin_data_path)

class MyBLiveClient(BLiveClient):
    # async def _on_receive_danmaku(self, danmaku: DanmakuMessage):
    #     username = danmaku.uname
    #     username_pinyin = re.sub("-", " ", pinyin.get_pinyin(danmaku.uname, tone_marks='marks'))
    #     print(f'{username}（{username_pinyin}）')

    async def _on_super_chat(self, message: SuperChatMessage):
        timestamp = datetime.now()
        username = message.uname
        username_pinyin = re.sub("-", " ", Pinyin().get_pinyin(message.uname, tone_marks='marks'))
        content = message.message
        self.log(f'{timestamp}: 醒目留言 ¥{message.price}\n{username}（{username_pinyin}）\n{content}\n')

    def log(self, s: str):
        # print('\033[1;40m\033[1;34m%s\033[0m\033[0m' % s)
        print (s)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(s)
            f.write('\n')

async def main():
    global room_id

    tmp = input('请输入直播间ID：')
    if tmp != "":
        room_id = int(tmp)

    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
