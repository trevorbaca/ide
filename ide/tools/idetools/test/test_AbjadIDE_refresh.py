import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_refresh_01():
    r'''In material directory.
    '''

    material_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        )
    ly_path = pathlib.Path(material_directory, 'illustration.ly')

    lines = [
        'Red Score (2017) - materials directory - magic numbers',
        '',
        '   1: __illustrate__.py',
        '   2: __init__.py',
        '   3: __metadata__.py',
        '   4: definition.py',
        '',
        '      copy (cp)',
        '      new (new)',
        '      remove (rm)',
        '      rename (ren)',
        '',
        '>',
        ]

    with ide.Test():
        assert ly_path.is_file()
        input_ = 'red~score mm magic~numbers !rm~illustration.ly rf q'
        abjad_ide._start(input_=input_)
        assert not ly_path.exists()

    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
