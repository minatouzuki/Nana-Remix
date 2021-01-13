from nana.plugins.database.lang_db import switch_to_locale, prev_locale
from nana.languages.strings import tld
from nana.languages.list_locale import list_locales
import re

from pyrogram import filters, errors
from pyrogram.types import InlineKeyboardButton

from pykeyboard import InlineKeyboard

from nana import setbot, Owner


async def language_button_callback(_, __, query):
    if re.match(r'set_lang_', query.data):
        return True


language_button_create = filters.create(language_button_callback)


@setbot.on_callback_query(language_button_create)
async def locale_button(_, query):
    lang_match = re.findall(
        r'en-US|hi|he|id|fa|el|dv|es|ja|de|ta|pt-br|ar|ku|tr',
        query.data,
    )
    if lang_match:
        if lang_match[0]:
            switch_to_locale(Owner, lang_match[0])
            await query.answer(
                text=tld('language_switch_success_pm').format(
                    list_locales[lang_match[0]],
                ),
                show_alert=True,
            )
        else:
            await query.answer(text='Error!', show_alert=True)
    try:
        LANGUAGE = prev_locale(Owner)
        locale = LANGUAGE.locale_name
        curr_lang = list_locales[locale]
    except Exception:
        curr_lang = 'English (US)'

    text = tld('language_select_language')
    text += tld('language_current_locale').format(curr_lang)
    buttons = InlineKeyboard()
    buttons.row(
        InlineKeyboardButton('US 🇺🇸', callback_data='set_lang_en-US'),
        InlineKeyboardButton('IN 🇮🇳', callback_data='set_lang_hi'),
        InlineKeyboardButton('HE 🇮🇱', callback_data='set_lang_he'),
        InlineKeyboardButton('ID 🇮🇩', callback_data='set_lang_id'),
        InlineKeyboardButton('FA 🇮🇷', callback_data='set_lang_fa'),
    )
    buttons.row(
        InlineKeyboardButton('JA 🇯🇵', callback_data='set_lang_ja'),
        InlineKeyboardButton('GR 🇬🇷', callback_data='set_lang_el'),
        InlineKeyboardButton('MV 🇲🇻', callback_data='set_lang_dv'),
        InlineKeyboardButton('ES 🇪🇸', callback_data='set_lang_es'),
        InlineKeyboardButton('DE 🇩🇪', callback_data='set_lang_de'),
    )
    buttons.row(
        InlineKeyboardButton('TA 🏴󠁩󠁮󠁴󠁮󠁿', callback_data='set_lang_ta'),
        InlineKeyboardButton('BR 🇧🇷', callback_data='set_lang_pt-br'),
        InlineKeyboardButton('AR 🇸🇦', callback_data='set_lang_pt-ar'),
        InlineKeyboardButton('CKB ☀️', callback_data='set_lang_pt-ku'),
        InlineKeyboardButton('TR 🇹🇷', callback_data='set_lang_pt-tr'),
    ),
    buttons.row(
        InlineKeyboardButton('◀️', callback_data='language_back'),
    )
    try:
        await query.message.edit(
            text,
            parse_mode='markdown',
            reply_markup=buttons,
        )
        await query.answer()
    except errors.exceptions.bad_request_400.MessageNotModified:
        return
