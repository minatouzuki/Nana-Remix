from nekobin import NekoBin
from nana import setbot
from nana import AdminSettings
from nana.utils.dynamic_filt import dynamic_data_filter

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton

from pykeyboard import InlineKeyboard


@setbot.on_message(
    filters.user(AdminSettings) &
    filters.command('logs'),
)
async def logs(_, message):
    keyboard = InlineKeyboard(row_width=1)
    keyboard.add(
        InlineKeyboardButton('~ Nekofy', callback_data='nekofy'),
    )
    await message.reply_document(
        'nana/logs/error.txt',
        caption='Here are your logs!',
        reply_markup=keyboard,
    )


@setbot.on_callback_query(dynamic_data_filter('nekofy'))
async def paste_log_neko(client, query):
    nekobin = NekoBin()
    if query.from_user.id in AdminSettings:
        f = open('nana/logs/error.txt')
        data = await nekobin.nekofy(f.read())
        keyb = InlineKeyboard(row_width=2)
        keyb.add(
            InlineKeyboardButton('URL', url=str(data.url)),
            InlineKeyboardButton('RAW', url=str(data.raw)),
        )
        await query.message.edit_caption(
            '🐱 **Successfully Nekofied ~**', reply_markup=keyb,
        )
    else:
        await client.answer_callback_query(
            query.id,
            'You are not Allowed to press this',
            show_alert=True,
        )
