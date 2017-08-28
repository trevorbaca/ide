import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_display_navigation_command_help_01():
    r'''In score directory.
    '''

    lines = [
        'Red Score (2017) - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_02():
    r'''In material directory.
    '''

    lines = [
        'Red Score (2017) - materials directory - magic numbers - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score mm magic~numbers ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_03():
    r'''In segment directory.
    '''

    lines = [
        'Red Score (2017) - segments directory - A - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score gg A ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_04():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - scores directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    back (-)',
        '    quit (q)',
        '',
        '>',
        ]
    input_ = '; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_05():
    r'''In materials directory.
    '''

    lines = [
        'Red Score (2017) - materials directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score mm ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_06():
    r'''In segments directory.
    '''

    lines = [
        'Red Score (2017) - segments directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score gg ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line


def test_AbjadIDE_display_navigation_command_help_07():
    r'''In stylesheets directory.
    '''

    lines = [
        'Red Score (2017) - stylesheets directory - navigation commands',
        '',
        '    display navigation command help (;)',
        '',
        '    go to scores directory (ss)',
        '',
        '    go to build directory (bb)',
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
        '',
        '>',
        ]
    input_ = 'red~score yy ; q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
