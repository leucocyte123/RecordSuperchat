# -*- coding: utf-8 -*-
from datetime import datetime

import asyncio

from blivedm.blivedm import BLiveClient, GiftMessage, GuardBuyMessage, SuperChatMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'kitzuki'
room_id = VtuberOfInterest[selected_vtuber]

gift_threshold = 0
filename = 'log.txt'

class MyBLiveClient(BLiveClient):
    _COMMAND_HANDLERS = BLiveClient._COMMAND_HANDLERS.copy()
    _COMMAND_HANDLERS['STOP_LIVE_ROOM_LIST'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_COUNT'] = None
    _COMMAND_HANDLERS['ONLINE_RANK_V2'] = None
    _COMMAND_HANDLERS['HOT_RANK_CHANGED'] = None

    async def _on_receive_gift(self, gift: GiftMessage):
        if gift.coin_type == 'gold' and gift.total_coin > gift_threshold:
            self.log(f'{datetime.now()}: {gift.uname} 赠送{gift.gift_name}x{gift.num}\t（{gift.total_coin / 1000}元）')

    async def _on_buy_guard(self, message: GuardBuyMessage):
        self.log(f'{datetime.now()}: {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: SuperChatMessage):
        self.log(f'{datetime.now()}: 醒目留言 ¥{message.price} {message.uname}：{message.message}')

    def log(self, s: str):
        print (s)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(s)
            f.write('\n')

async def main():
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
