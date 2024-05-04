import asyncio
from datetime import datetime, timedelta

from telethon.errors.rpcerrorlist import RPCError
from telethon.tl.types import Message

from .. import loader, utils


from hikka import Hikka, commands
import random

hikka = Hikka()

@commands.command("roll")
async def roll_dice(message, max_value: int):
    if max_value <= 0:
        await message.reply("Максимальное число должно быть больше нуля!")
        return
    result = random.randint(1, max_value)
    await message.reply(f"Выпало число: {result}")

if __name__ == "__main__":
    hikka.add_command(roll_dice)
    hikka.run()
    