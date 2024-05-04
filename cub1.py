import asyncio
from datetime import datetime

from telethon.errors.rpcerrorlist import RPCError
from telethon.tl.types import Message


from telethon.sync import TelegramClient, events
import random



client = TelegramClient

@client.on(events.NewMessage(pattern='/roll'))
async def roll(event):
    try:
        max_value = int(event.raw_text.split()[1])
        result = roll_dice(max_value)
        await event.respond(f'Выпало число: {result}')
    except Exception as e:
        await event.respond('Ошибка! Укажите максимальное число после команды /roll.')

def roll_dice(max_value):
    return random.randint(1, max_value)

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
    