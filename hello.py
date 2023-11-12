import asyncio
import telegram


async def main():
    bot = telegram.Bot("6336304373:AAG4zaeQ4EyejWNC59zzCid-i-odrKAtVP0")
    async with bot:
        print((await bot.get_updates())[0])
        await bot.send_message(text='Hi John!', chat_id=186312121)


if __name__ == '__main__':
    asyncio.run(main())
