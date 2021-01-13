from codecs import decode
from codecs import encode

import yaml

from nana import logging as LOGGER
from nana import Owner
from nana.plugins.database.lang_db import prev_locale

LANGUAGES = [
    'en-US',
    'hi',
    'he',
    'id',
    'fa',
    'el',
    'dv',
    'es',
    'ja',
    'de',
    'ta',
    'pt-br',
    'ar',
    'ku',
    'tr',
]

strings = {
    i: yaml.full_load(
        open('locales/' + i + '.yml'),
    ) for i in LANGUAGES
}


def tld(t, _show_none=True):
    LANGUAGE = prev_locale(Owner)
    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            result = decode(
                encode(strings['en-US'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('hi') and t in strings['hi']:
            result = decode(
                encode(strings['hi'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('he') and t in strings['he']:
            result = decode(
                encode(strings['he'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('id') and t in strings['id']:
            result = decode(
                encode(strings['id'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('fa') and t in strings['fa']:
            result = decode(
                encode(strings['fa'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('el') and t in strings['el']:
            result = decode(
                encode(strings['el'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('dv') and t in strings['dv']:
            result = decode(
                encode(strings['dv'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('es') and t in strings['es']:
            result = decode(
                encode(strings['es'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('ja') and t in strings['ja']:
            result = decode(
                encode(strings['ja'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('de') and t in strings['de']:
            result = decode(
                encode(strings['de'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('ta') and t in strings['ta']:
            result = decode(
                encode(strings['ta'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('pt-br') and t in strings['pt-br']:
            result = decode(
                encode(strings['pt-br'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('ar') and t in strings['ar']:
            result = decode(
                encode(strings['ar'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('ku') and t in strings['ku']:
            result = decode(
                encode(strings['ku'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result
        elif LOCALE in ('tr') and t in strings['tr']:
            result = decode(
                encode(strings['tr'][t], 'latin-1', 'backslashreplace'),
                'unicode-escape',
            )
            return result

    if t in strings['en-US']:
        result = decode(
            encode(
                strings['en-US'][t],
                'latin-1',
                'backslashreplace',
            ),
            'unicode-escape',
        )
        return result

    err = f'No string found for {t}.\nReport it in @nanabotsupport.'
    LOGGER.warning(err)
    return err


def tld_list(t):
    LANGUAGE = prev_locale(Owner)

    if LANGUAGE:
        LOCALE = LANGUAGE.locale_name
        if LOCALE in ('en-US') and t in strings['en-US']:
            return strings['en-US'][t]
        elif LOCALE in ('hi') and t in strings['hi']:
            return strings['hi'][t]
        elif LOCALE in ('he') and t in strings['he']:
            return strings['he'][t]
        elif LOCALE in ('id') and t in strings['id']:
            return strings['id'][t]
        elif LOCALE in ('fa') and t in strings['fa']:
            return strings['fa'][t]
        elif LOCALE in ('el') and t in strings['el']:
            return strings['el'][t]
        elif LOCALE in ('dv') and t in strings['dv']:
            return strings['dv'][t]
        elif LOCALE in ('es') and t in strings['es']:
            return strings['es'][t]
        elif LOCALE in ('ja') and t in strings['ja']:
            return strings['ja'][t]
        elif LOCALE in ('de') and t in strings['de']:
            return strings['de'][t]
        elif LOCALE in ('ta') and t in strings['ta']:
            return strings['ta'][t]
        elif LOCALE in ('pt-br') and t in strings['pt-br']:
            return strings['pt-br'][t]
        elif LOCALE in ('ar') and t in strings['ar']:
            return strings['ar'][t]
        elif LOCALE in ('ku') and t in strings['ku']:
            return strings['ku'][t]
        elif LOCALE in ('tr') and t in strings['tr']:
            return strings['tr'][t]

    if t in strings['en-US']:
        return strings['en-US'][t]

    LOGGER.warning(f'#NOSTR No string found for {t}.')
    return f'No string found for {t}.\nReport it in @nanabotsupport.'
