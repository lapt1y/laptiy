import asyncio
from datetime import datetime, timedelta

from telethon.errors import RPCError, FloodWaitError
from telethon.tl.types import Message

from .. import loader, utils

TARGET_DATE = datetime(2024, 5, 10)
API_WAIT_TIME = 10  # seconds

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
        custom_text = utils.get_args_raw(message)
        try:
            m = await self.animate_countdown(
                message,
                custom_text,
                interval=0.059,
                inline=False,
            )
            await m.edit(utils.escape_html(custom_text) + "\n<b>" + custom_text + "</b>" + "\n" + "No custom text provided")
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Skip handling this error
            else:
                raise e  # Raise error if it's a different RPC error

    async def countdownicmd(self, message: Message):
        """Shows time until May 10th [Inline]"""
        custom_text = utils.get_args_raw(message)
        try:
            m = await self.animate_countdown(
                message,
                custom_text,
                interval=0.059,
                inline=True,
            )
            await m.edit(utils.escape_html(custom_text) + "\n<b>" + custom_text + "</b>" + "\n" + "No custom text provided")
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 1)
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Skip handling this error
            else:
                raise e  # Raise error if it's a different RPC error

    async def animate_countdown(self, message: Message, custom_text: str, interval: float, inline: bool):
        m = None
        while True:
            delta = TARGET_DATE - datetime.now()
            if delta.total_seconds() <= 0:
                break
            countdown_text = self.strfdelta(delta)
            try:
                m = await self.edit_message(
                    message,
                    m,
                    custom_text + "\n<b>" + countdown_text + "</b>" if custom_text else "<b>" + countdown_text + "</b>",
                    inline=inline,
                )
            except FloodWaitError as e:
                await asyncio.sleep(e.seconds + 1)
            await asyncio.sleep(interval)
        return m

    async def edit_message(self, message: Message, m: Message, text: str, inline: bool):
        try:
            if m:
                await m.edit(text, parse_mode='html')
            else:
                m = await message.respond(text, parse_mode='html', link_preview=False)
        except RPCError as e:
            if isinstance(e, FloodWaitError):
                await asyncio.sleep(e.seconds + 1)
            else:
                raise e
        return m

    def strfdelta(self, tdelta: timedelta) -> str:
        seconds = tdelta.total_seconds()
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} min, {int(seconds)} sec"
        