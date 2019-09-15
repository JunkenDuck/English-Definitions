from json import JSONDecodeError

from aqt import mw
from anki.hooks import addHook
from . import definitions

config = mw.addonManager.getConfig(__name__)

WORD_FIELD = config['word_field']
DEF_FIELD = config['def_field']
GOOGLE_SHORTCUT = config['google_shortcut']
WEBSTER_SHORTCUT = config['webster_shortcut']


class DefFail(Exception):
    pass


def insert_definition(editor, dictionary: str):
    n = editor.note
    # print(n['Definition'])
    # return
    try:
        if dictionary == 'google':
            n[DEF_FIELD] = definitions.GoogleDefinition(n[WORD_FIELD]).format_def().replace('\n', '<br>')
        elif dictionary == 'webster':
            definition = definitions.WebstersDefinition(n[WORD_FIELD]).format_def().replace('\n', '<br>')
            if len(definition) == 0:
                raise DefFail
            n[DEF_FIELD] = definition
    except (JSONDecodeError, DefFail):
        n[DEF_FIELD] = 'Failed to fetch word'
    editor.loadNote()


def add_button(buttons, editor):
    buttons.insert(0, editor.addButton(
        icon=None,
        cmd='insert_webster',
        func=lambda ed: insert_definition(ed, 'webster'),
        tip="Adds definition using Webster's dictionary\nShortcut: " + WEBSTER_SHORTCUT,
        label="W",
        id="W"
    ))
    buttons.insert(0, editor.addButton(
        icon=None,
        cmd='insert_google',
        func=lambda ed: insert_definition(ed, 'google'),
        tip='Adds definition using Google\'s dictionary\nShortcut: ' + GOOGLE_SHORTCUT,
        label="G",
        id="G"
    ))

    return buttons


def setup_shortcuts(shortcuts, editor):
    shortcuts.append((GOOGLE_SHORTCUT, lambda: insert_definition(editor, 'google')))
    shortcuts.append((WEBSTER_SHORTCUT, lambda: insert_definition(editor, 'webster')))


addHook("setupEditorButtons", add_button)
addHook("setupEditorShortcuts", setup_shortcuts)
