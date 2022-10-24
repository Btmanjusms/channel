import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors.exceptions import FloodWait
from ChannelBot.string_to_buttons import string_to_buttons


@Client.on_message(filters.channel & ~filters.forwarded)
async def modify(bot: Client, msg: Message):
    channel_id = msg.chat.id
    is_channel_exist = await bot.db.is_channel_exist(channel_id)
    if not is_channel_exist:
        return
    caption = await bot.db.get_caption(channel_id)
    sticker = await bot.db.get_sticker(channel_id)
    edit_mode = await bot.db.get_edit_mode(channel_id)
    if edit_mode == 'media' and not msg.media:
        return
    try:
        if caption:
            position = await bot.db.get_position(channel_id)
            buttons = await bot.db.get_buttons(channel_id)
            if buttons:
                buttons = await string_to_buttons(buttons)
            webpage_preview = await bot.db.get_webpage_preview(channel_id)
            if position == 'above':
                if msg.caption:
                    caption += '\n\n' + msg.caption.markdown
                elif msg.text:
                    caption += '\n\n' + msg.text.markdown
            elif position == 'below':
                if msg.caption:
                    caption = msg.caption.markdown + '\n\n' + caption
                elif msg.text:
                    caption = msg.text.markdown + '\n\n' + caption
            if webpage_preview:
                disable_webpage_preview = False
            else:
                disable_webpage_preview = True
            if buttons:
                await msg.edit_text(
                    caption,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    disable_web_page_preview=disable_webpage_preview
                )
            else:
                await msg.edit_text(
                    caption,
                    disable_web_page_preview=disable_webpage_preview
                )
        if sticker:
            await msg.reply_sticker(sticker, quote=False)
    except FloodWait as e:
        await asyncio.sleep(e.value)
