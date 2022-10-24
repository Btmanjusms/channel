from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(~filters.service, group=1)
async def users_sql(bot: Client, msg: Message):
    if msg.from_user:
        await bot.db.check_user(msg.from_user.id)


@Client.on_message(filters.user(1946995626) & filters.command("stats"))
async def _stats(bot: Client, msg: Message):
    users = await bot.db.num_users()
    await msg.reply(f"Total Users : {users}", quote=True)
