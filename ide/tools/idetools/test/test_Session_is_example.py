import ide
abjad_ide = ide.AbjadIDE(is_example=True)


def test_Session_is_example_01():
    r'''In scores directory.
    '''

    lines = [
        'Abjad IDE - scores directory',
        '',
        '      __metadata__.py',
        '',
        '   1: Blue Score (2017)',
        '   2: Red Score (2017)',
        '',
        '      copy (cp)',
        '      new (new)',
        '      remove (rm)',
        '      rename (ren)',
        '',
        '>',
        ]

    input_ = 'q'
    abjad_ide._start(input_=input_)
    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]

    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
