import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_display_navigation_help_01():
    r'''In library.
    '''

    if not abjad_ide._get_library():
        return

    abjad_ide('lib ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Abjad IDE : library : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_02():
    r'''In material directory.
    '''

    abjad_ide('red~score mm magic ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : materials : magic_numbers : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_03():
    r'''In materials directory.
    '''

    abjad_ide('red~score mm ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : materials : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_04():
    r'''In score directory.
    '''

    abjad_ide('red~score ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_05():
    r'''In scores directory.
    '''

    abjad_ide('; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Abjad IDE : scores : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_06():
    r'''In segment directory.
    '''

    abjad_ide('red~score gg A ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : segments : A : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_07():
    r'''In segments directory.
    '''

    abjad_ide('red~score gg ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : segments : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    go to next package (>)',
        '    go to previous package (<)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_


def test_AbjadIDE_display_navigation_help_08():
    r'''In stylesheets directory.
    '''

    abjad_ide('red~score yy ; q')
    menu = abjad_ide.io.transcript.menus[-1]
    menu_ = [
        'Red Score (2017) : stylesheets : navigation commands',
        '',
        '    display navigation help (;)',
        '',
        '    go to library (lib)',
        '    go to scores directory (ss)',
        '',
        '    go to builds directory (bb)',
        '    go to builds segments directory (nn)',
        '    go to contents directory (cc)',
        '    go to distribution directory (dd)',
        '    go to etc directory (ee)',
        '    go to materials directory (mm)',
        '    go to segments directory (gg)',
        '    go to stylesheets directory (yy)',
        '    go to test directory (tt)',
        '    go to tools directory (oo)',
        '    go to wrapper directory (ww)',
        '',
        '    back (-)',
        '    quit (q)',
        '    up (..)',
        '',
        ]
    for line, line_ in zip(menu, menu_):
        assert line == line_
