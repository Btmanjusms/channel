from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_chat_join_request(filters.group | filters.channel)
async def autoapprove(bot: Client, msg: Message):
    try:
        await bot.approve_chat_join_request(msg.chat.id, msg.from_user.id)
    except Exception as e:
        print('Error: ', e)
