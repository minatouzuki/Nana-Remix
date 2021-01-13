import re

import speedtest
from pyrogram import filters

from nana import AdminSettings
from nana import app
from nana import BotUsername
from nana import COMMAND_PREFIXES
from nana import setbot
from nana.languages.strings import tld
from nana.utils.Pyroutils import ReplyCheck


def speedtest_callback(_, __, query):
    if re.match('speedtest', query.data):
        return True


speedtest_create = filters.create(speedtest_callback)


def speed_convert(size):
    """Hi human, you can't read bytes?"""
    power = 2 ** 10
    zero = 0
    units = {0: '', 1: 'Kb/s', 2: 'Mb/s', 3: 'Gb/s', 4: 'Tb/s'}
    while size > power:
        size /= power
        zero += 1
    return f'{round(size, 2)} {units[zero]}'


@setbot.on_callback_query(speedtest_create)
async def speedtestxyz_callback(client, query):
    if query.from_user.id in AdminSettings:
        await client.edit_inline_text(
            query.inline_message_id, tld('speed_test_running'),
        )
        speed = speedtest.Speedtest()
        speed.get_best_server()
        speed.download()
        speed.upload()
        replymsg = tld('speed_test_result')
        if query.data == 'speedtest_image':
            speedtest_image = speed.results.share()
            replym = (
                '{}[\u200c\u200c\u200e]({})'.format(
                    tld('speed_test_result'),
                    speedtest_image,
                )
            )
            await client.edit_inline_text(
                query.inline_message_id,
                replym,
                parse_mode='markdown',
            )

        elif query.data == 'speedtest_text':
            result = speed.results.dict()
            replymsg += '\n - {} `{}`'.format(
                tld('speed_test_isp'),
                result['client']['isp'],
            )
            replymsg += '\n - {} `{}`'.format(
                tld('speed_test_download'),
                speed_convert(result['download']),
            )
            replymsg += (
                '\n - {} `{}`'.format(
                    tld('speed_test_upload'),
                    speed_convert(result['upload']),
                )
            )
            replymsg += f"\n - {tld('speed_test_ping')} `{result['ping']}`"
            await client.edit_inline_text(
                query.inline_message_id, replymsg,
            )

    else:
        await client.answer_callback_query(
            query.id, 'No, you are not allowed to do this', show_alert=False,
        )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('speedtest', COMMAND_PREFIXES),
)
async def speed_test_inline(client, message):
    x = await client.get_inline_bot_results(f'{BotUsername}', 'speedtest')
    await message.delete()
    await client.send_inline_bot_result(
        chat_id=message.chat.id,
        query_id=x.query_id,
        result_id=x.results[0].id,
        reply_to_message_id=ReplyCheck(message),
        hide_via=True,
    )
