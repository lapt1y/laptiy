import asyncio
from datetime import datetime

from telethon.errors.rpcerrorlist import RPCError
from telethon.tl.types import Message

from .. import loader, utils

TARGET_DATE = datetime(2024, 5, 10)

@loader.tds
class Countdown(loader.Module):
    """Countdown to May 10th"""

    strings = {"name": "Countdown"}
    strings_ru = {
        "_cls_doc": "Обратный отсчёт до 10 мая",
        "_cmd_doc_countdown": "Показывает время до 10 мая",
    }

    async def countdowncmd(self, message: Message):
        """Shows time until May 10th"""
        try:
            m = await self.animate_countdown(
                message,
                interval=0.059,
                inline=False,
            )
            await m.edit(utils.get_args_raw(message) or "❤️")
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Skip handling this error
            else:
                raise e  # Raise error if it's a different RPC error

    async def countdownicmd(self, message: Message):
        """Shows time until May 10th [Inline]"""
        try:
            m = await self.animate_countdown(
                message,
                interval=0.059,
                inline=True,
            )
            await m.edit(utils.get_args_raw(message) or "❤️")
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Skip handling this error
            else:
                raise e  # Raise error if it's a different RPC error

    async def animate_countdown(self, message: Message, interval: float, inline: bool):
        while True:
            delta = TARGET_DATE - datetime.now()
            if delta.total_seconds() <= 0:
                break
            countdown_text = str(delta).split(".")[0]
            m = await self.edit_message(
                message,
                countdown_text,
                inline=inline,
            )
            await asyncio.sleep(interval)
        return m

    async def edit_message(self, message: Message, text: str, inline: bool):
        try:
            await message.edit(text)
        except:
            m = await message.respond(text, parse_mode=None, link_preview=False)
            await asyncio.sleep(0.5)
            await m.delete()
        return m
        