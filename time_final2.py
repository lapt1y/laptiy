import asyncio
from datetime import datetime, timedelta

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

    

    async def laptiytime(self, message: Message, inline: bool):
        custom_text = utils.get_args_raw(message)
        try:
            await asyncio.sleep(1)  # ограничение на один запрос в секунду
            m = await self.animate_laptiytime(
                message,
                custom_text,
                interval=60,
                inline=inline,
            )
            await m.edit(utils.escape_html(custom_text) + "\n<b>" + custom_text + "</b>" + "\n" + "No custom text provided")
        except RPCError as e:
            if "Content of the message was not modified" in str(e):
                pass  # Skip handling this error
            else:
                raise e  # Raise error if it's a different RPC error

    async def animate_laptiytime(self, message: Message, custom_text: str, interval: float, inline: bool):
        m = None
        while True:
            delta = TARGET_DATE - datetime.now()
            if delta.total_seconds() <= 0:
                break
            laptiytime_text = self.strfdelta(delta)
            await asyncio.sleep(1)  # ограничение на один запрос в секунду
            m = await self.edit_message(
                message,
                m,
                custom_text + "\n<b>" + laptiytime_text + "</b>" if custom_text else "<b>" + laptiytime_text + "</b>",
                inline=inline,
            )
            await asyncio.sleep(interval)
        return m

    async def edit_message(self, message: Message, m: Message, text: str, inline: bool):
        try:
            if m:
                await m.edit(text, parse_mode='html')
            else:
                m = await message.respond(text, parse_mode='html', link_preview=False)
        except:
            pass
        return m

    def strfdelta(self, tdelta: timedelta) -> str:
        seconds = tdelta.total_seconds()
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        return f"{int(days)} days, {int(hours)} hours, {int(minutes)} min"
        