import asyncio
from datetime import datetime

from telethon.errors.rpcerrorlist import RPCError
from telethon.tl.types import Message

from .. import loader, utils

TARGET_DATE = datetime(2024, 5, 10)

@loader.tds
class laptiytime(loader.Module):
    """laptiytime to May 10th"""

    strings = {"name": "laptiytime"}
    strings_ru = {
        "_cls_doc": "Обратный отсчёт до 10 мая",
        "_cmd_doc_laptiytime": "Показывает время до 10 мая",
    }

    async def laptiytimecmd(self, message: Message):
        """Shows time until May 10th"""
        try:
            m = await self.animate_laptiytime(
                message,
                interval=0.001,
                inline=False,
            )
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Пропустить обработку этой ошибки
            else:
                raise e  # Вызвать ошибку, если это другая RPC ошибка

    async def laptiytimeicmd(self, message: Message):
        """Shows time until May 10th [Inline]"""
        try:
            m = await self.animate_laptiytime(
                message,
                interval=0.001,
                inline=True,
            )
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Пропустить обработку этой ошибки
            else:
                raise e  # Вызвать ошибку, если это другая RPC ошибка

    async def animate_laptiytime(self, message: Message, interval: float, inline: bool):
        while True:
            delta = TARGET_DATE - datetime.now()
            if delta.total_seconds() <= 0:
                break
            laptiytime_text = str(delta).split(".")[0]
            await message.edit(laptiytime_text)
            await asyncio.sleep(interval)
            