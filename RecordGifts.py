# -*- coding: utf-8 -*-

import asyncio

from blivedm.blivedm import BLiveClient, GiftMessage, GuardBuyMessage, SuperChatMessage

VtuberOfInterest = {
    'xuehusang': 24393,
    'kitzuki': 22889484,
}

selected_vtuber = 'kitzuki'
room_id = VtuberOfInterest[selected_vtuber]

class MyBLiveClient(BLiveClient):
    async def _on_receive_gift(self, gift: GiftMessage):
        print(f'{gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.coin_type}币x{gift.total_coin}）')

    async def _on_buy_guard(self, message: GuardBuyMessage):
        print(f'{message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: SuperChatMessage):
        print(f'醒目留言 ¥{message.price} {message.uname}：{message.message}')

async def main():
    client = MyBLiveClient(room_id, ssl=True)
    future = client.start()
    try:
        await future
    finally:
        await client.close()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
