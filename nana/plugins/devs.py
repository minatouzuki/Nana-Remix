import os
import re
import subprocess
import sys
import traceback
from io import StringIO

from pyrogram import filters

from nana import COMMAND_PREFIXES, app, edit_or_reply, AdminSettings
from nana.utils.parser import mention_markdown
from nana.utils.aiohttp_helper import AioHttp

__MODULE__ = 'Devs'
__HELP__ = """
This module is for those who know programming or
getting some technical information about your (user)bot or user account.

──「 **Python** 」──
-> `eval (command)`
Run Python code

──「 **Shell** 」──
-> `sh (command)`
Execute shell commands

──「 **Take log** 」──
-> `log`
Upload the recent logs on nekobin and send it

──「 **Data Centers** 」──
-> `dc`
Get your DC

──「 **Testing The Internet Speed Of Your Server** 」──
-> `speedtest`
See internet speed and some other info

──「 **IDs** 」──
-> `id`
Send ID of what you replied to

──「 **Self Destruct Reveal** 」──
-> `reveal` or `reveal self`
Reveal Self Destruct photo untouched,
'self' tag will reveal it in Saved Messages
"""


async def aexec(code, client, message):
    exec(
        'async def __aexec(client, message): '
        + ''.join(f'\n {a}' for a in code.split('\n')),
    )
    return await locals()['__aexec'](client, message)


@app.on_message(filters.me & filters.command('reveal', COMMAND_PREFIXES))
async def sd_reveal(client, message):
    cmd = message.command
    self_tag = ' '.join(cmd[1:])
    tags = 'self' in self_tag
    if len(message.text.split()) == 1:
        await message.delete()
        return
    await message.delete()
    a = 'nana/file.png'
    await client.download_media(message.reply_to_message.photo, file_name=a)
    if tags:
        await client.send_photo('me', a)
    else:
        await client.send_photo(message.chat.id, a)

    os.remove(a)


@app.on_message(
    filters.user(AdminSettings)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command('eval', COMMAND_PREFIXES),
)
async def executor(client, message):
    try:
        cmd = message.text.split(' ', maxsplit=1)[1]
    except IndexError:
        await message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ''
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = 'Success'
    final_output = (
        '**Input**:\n```{}```\n\n**Result**:\n```{}```'.format(
            cmd,
            evaluation.strip(),
        )
    )
    if len(final_output) > 4096:
        filename = 'output.txt'
        with open(filename, 'w+', encoding='utf8') as out_file:
            out_file.write(str(evaluation.strip()))
        await message.reply_document(
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await message.delete()
    else:
        await edit_or_reply(
            message,
            text=final_output,
            parse_mode='markdown',
        )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('ip', COMMAND_PREFIXES),
)
async def public_ip(_, message):
    j = await AioHttp().get_json('http://ip-api.com/json')
    stats = f"**ISP {j['isp']}:**\n"
    stats += f"**AS:** `{j['as']}`\n"
    stats += f"**IP Address:** `{j['query']}`\n"
    stats += f"**Country:** `{j['country']}`\n"
    stats += f"**Zip code:** `{j['zip']}`\n"
    stats += f"**Lattitude:** `{j['lat']}`\n"
    stats += f"**Longitude:** `{j['lon']}`\n"
    stats += f"**Time Zone:** `{j['timezone']}`"
    await edit_or_reply(message, text=stats, parse_mode='markdown')


@app.on_message(
    filters.user(AdminSettings)
    & ~filters.forwarded
    & ~filters.via_bot
    & filters.command('sh', COMMAND_PREFIXES),
)
async def terminal(client, message):
    if len(message.text.split()) == 1:
        await edit_or_reply(message, text='Usage: `sh ping -c 5 google.com`')
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if '\n' in teks:
        code = teks.split('\n')
        output = ''
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await edit_or_reply(
                    message,
                    text="""
**Input:**
```{}```

**Error:**
```{}```
""".format(
                        teks, err,
                    ),
                )
            output += f'**{code}**\n'
            output += process.stdout.read()[:-1].decode('utf-8')
            output += '\n'
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', '')
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            await edit_or_reply(
                message,
                text="""**Input:**\n```{}```\n\n**Error:**\n```{}```""".format(
                    teks, ''.join(errors),
                ),
            )
            return
        output = process.stdout.read()[:-1].decode('utf-8')
    if str(output) == '\n':
        output = None
    if output:
        if len(output) > 4096:
            with open('nana/cache/output.txt', 'w+') as file:
                file.write(output)
                file.close()
            await client.send_document(
                message.chat.id,
                'nana/cache/output.txt',
                reply_to_message_id=message.message_id,
                caption='`Output`',
            )
            os.remove('nana/cache/output.txt')
            return
        await edit_or_reply(
            message,
            text="""**Input:**\n```{}```\n\n**Output:**\n```{}```""".format(
                teks, output,
            ),
        )
    else:
        await edit_or_reply(
            message,
            text='**Input: **\n`{}`\n\n**Output: **\n`No output`'.format(
                teks,
            ),
        )


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('dc', COMMAND_PREFIXES),
)
async def dc_id_check(_, message):
    user = message.from_user
    if message.reply_to_message:
        if message.reply_to_message.forward_from:
            dc_id = message.reply_to_message.forward_from.dc_id
            user = mention_markdown(
                message.reply_to_message.forward_from.id,
                message.reply_to_message.forward_from.first_name,
            )
        else:
            dc_id = message.reply_to_message.from_user.dc_id
            user = mention_markdown(
                message.reply_to_message.from_user.id,
                message.reply_to_message.from_user.first_name,
            )
    else:
        dc_id = user.dc_id
        user = mention_markdown(
            message.from_user.id,
            message.from_user.first_name,
        )
    if dc_id == 1:
        text = "{}'s assigned DC is **DC1**, **MIA, Miami FL, USA**".format(
            user,
        )
    elif dc_id == 2:
        text = "{}'s assigned DC is **DC2**, **AMS, Amsterdam, NL**".format(
            user,
        )
    elif dc_id == 3:
        text = "{}'s assigned DC is **DC3**, **MIA, Miami FL, USA**".format(
            user,
        )
    elif dc_id == 4:
        text = "{}'s assigned DC is **DC4**, **AMS, Amsterdam, NL**".format(
            user,
        )
    elif dc_id == 5:
        text = "{}'s assigned DC is **DC5**, **SIN, Singapore, SG**".format(
            user,
        )
    else:
        text = f"{user}'s assigned DC is **unknown**"
    await edit_or_reply(message, text=text)


@app.on_message(
    filters.user(AdminSettings) &
    filters.command('id', COMMAND_PREFIXES),
)
async def get_id(_, message):
    file_id = None
    user_id = None
    if message.reply_to_message:
        rep = message.reply_to_message
        if rep.audio:
            file_id = f'**File ID**: `{rep.audio.file_id}`\n'
            file_id += '**File type**: `audio`\n'
        elif rep.document:
            file_id = f'**File ID**: `{rep.document.file_id}`\n'
            file_id += f'**File type**: `{rep.document.mime_type}`\n'
        elif rep.photo:
            file_id = f'**File ID**: `{rep.photo.file_id}`\n'
            file_id += '**File type**: `photo`'
        elif rep.sticker:
            file_id = f'**Sicker ID**: `{rep.sticker.file_id}`\n'
            if rep.sticker.set_name and rep.sticker.emoji:
                file_id += '**Sticker set**: `{}`\n'.format(
                    rep.sticker.set_name,
                )
                file_id += f'**Sticker emoji**: `{rep.sticker.emoji}`\n'
                if rep.sticker.is_animated:
                    file_id += '**Animated sticker**: `{}`\n'.format(
                        rep.sticker.is_animated,
                    )
                else:
                    file_id += '**Animated sticker**: `False`\n'
            else:
                file_id += '**Sticker set**: __None__\n'
                file_id += '**Sticker emoji**: __None__'
        elif rep.video:
            file_id = f'**File ID**: `{rep.video.file_id}`\n'
            file_id += '**File type**: `video`'
        elif rep.animation:
            file_id = f'**File ID**: `{rep.animation.file_id}`\n'
            file_id += '**File type**: `GIF`'
        elif rep.voice:
            file_id = f'**File ID**: `{rep.voice.file_id}`\n'
            file_id += '**File type**: `voice note`'
        elif rep.video_note:
            file_id = f'**File ID**: `{rep.animation.file_id}`\n'
            file_id += '**File type**: `video note`'
        elif rep.location:
            file_id = '**Location**:\n'
            file_id += f'    **Longitude**: `{rep.location.longitude}`\n'
            file_id += f'    **Latitude**: `{rep.location.latitude}`'
        elif rep.venue:
            file_id = '**Location**:\n'
            file_id += f'    **Longitude**: `{rep.venue.location.longitude}`\n'
            file_id += f'    **Latitude**: `{rep.venue.location.latitude}`\n\n'
            file_id += '**Address**:\n'
            file_id += f'    **Title**: `{rep.venue.title}`\n'
            file_id += f'    **Detail**: `{rep.venue.address}`\n\n'
        elif rep.from_user:
            user_id = rep.from_user.id
    if user_id:
        if rep.forward_from:
            user_detail = (
                '**Forwarded from user ID**: `{}`\n'.format(
                    message.reply_to_message.forward_from.id,
                )
            )
        else:
            user_detail = '**User ID**: `{}`\n'.format(
                message.reply_to_message.from_user.id,
            )
        user_detail += '**Message ID**: `{}`'.format(
            message.reply_to_message.message_id,
        )
        await edit_or_reply(message, text=user_detail)
    elif file_id:
        if rep.forward_from:
            user_detail = (
                '**Forwarded from user ID**: `{}`\n'.format(
                    message.reply_to_message.forward_from.id,
                )
            )
        else:
            user_detail = '**User ID**: `{}`\n'.format(
                message.reply_to_message.from_user.id,
            )
        user_detail += '**Message ID**: `{}`\n\n'.format(
            message.reply_to_message.message_id,
        )
        user_detail += file_id
        await edit_or_reply(message, text=user_detail)
    else:
        await edit_or_reply(message, text=f'**Chat ID**: `{message.chat.id}`')
