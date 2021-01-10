from platform import python_version

from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardButton
from pykeyboard import InlineKeyboard
from nana import (
    AdminSettings,
    setbot,
    app,
    USERBOT_VERSION,
    ASSISTANT_VERSION,
    DB_AVAILABLE,
    NANA_IMG,
)
from nana.__main__ import reload_userbot, restart_all
from nana.utils.dynamic_filt import dynamic_data_filter
from nana.languages.strings import tld


async def is_userbot_run():
    try:
        return await app.get_me()
    except ConnectionError:
        return None


async def get_text_settings():
    me = await is_userbot_run()
    if not me:
        text = tld('settings_userbot_stop').format(USERBOT_VERSION)
    else:
        text = tld('settings_userbot_running').format(USERBOT_VERSION)
    text += tld('settings_assistant_running').format(ASSISTANT_VERSION)
    text += tld('settings_database').format(DB_AVAILABLE)
    text += tld('settings_python').format(python_version())
    return text


async def get_button_settings():
    me = await is_userbot_run()
    toggle = (
        tld('settings_userbot_stopbutton')
        if me
        else tld('settings_userbot_startbutton')
    )
    list_button = InlineKeyboard(row_width=2)
    list_button.add(
        InlineKeyboardButton(toggle, callback_data='toggle_startbot'),
        InlineKeyboardButton(
            tld('settings_userbot_restartbutton'),
            callback_data='restart_bot',
        ),
        InlineKeyboardButton(
            tld('settings_setstickerbutton'), callback_data='setsticker',
        ),
        InlineKeyboardButton(
            tld('language_btn'), callback_data='set_lang_',
        ),
        InlineKeyboardButton(
            'Select Branch',
            callback_data='change_branches',
        ),
    )
    return list_button


@setbot.on_message(
    filters.user(AdminSettings) &
    filters.command(['settings']) &
    filters.private,
)
async def settings(_, message):
    text = await get_text_settings()
    button = await get_button_settings()
    if NANA_IMG:
        await message.reply_photo(NANA_IMG, caption=text, reply_markup=button)
    else:
        await message.reply(text, reply_markup=button)


@setbot.on_callback_query(dynamic_data_filter('toggle_startbot'))
async def start_stop_bot(client, query):
    try:
        await app.stop()
    except ConnectionError:
        await reload_userbot()
        text = await get_text_settings()
        button = await get_button_settings()
        text += tld('settings_stats_botstart')
        try:
            await query.message.edit_text(text, reply_markup=button)
        except errors.exceptions.bad_request_400.MessageNotModified:
            pass
        await client.answer_callback_query(
            query.id,
            tld('settings_stats_botstart'),
        )
        return
    text = await get_text_settings()
    button = await get_button_settings()
    text += tld('settings_stats_botstop')
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(query.id, tld('settings_stats_botstop'))


@setbot.on_callback_query(dynamic_data_filter('restart_bot'))
async def reboot_bot(client, query):
    try:
        await restart_all()
    except ConnectionError:
        await client.answer_callback_query(
            query.id, tld('settings_bot_stoprestart_err'),
        )
        return
    text = await get_text_settings()
    text += tld('settings_stats_botrestart')
    button = await get_button_settings()
    try:
        await query.message.edit_text(text, reply_markup=button)
    except errors.exceptions.bad_request_400.MessageNotModified:
        pass
    await client.answer_callback_query(
        query.id,
        tld('settings_bot_restarting'),
    )


@setbot.on_callback_query(dynamic_data_filter('back'))
async def back(_, message):
    text = await get_text_settings()
    button = await get_button_settings()
    if NANA_IMG:
        await message.reply_photo(NANA_IMG, caption=text, reply_markup=button)
    else:
        await message.reply(text, reply_markup=button)
