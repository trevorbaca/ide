import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_refresh_01():
    r'''In material directory.
    '''

    material_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(material_directory, 'illustration.ly')

    lines = [
        'Red Example Score (2013) - materials directory - magic numbers',
        '',
        '   1: __illustrate__.py',
        '   2: __init__.py',
        '   3: __metadata__.py',
        '   4: definition.py',
        '   5: illustration.pdf',
        '',
        '      copy (cp)',
        '      new (new)',
        '      remove (rm)',
        '      rename (ren)',
        '',
        '>',
        ]

    with abjad.FilesystemState(keep=[ly_path]):
        assert os.path.isfile(ly_path)
        input_ = 'red~example~score mm magic~numbers !rm~illustration.ly rf q'
        abjad_ide._start(input_=input_)
        assert not os.path.exists(ly_path)

    transcript_entry = abjad_ide._io_manager._transcript.entries[-3]
    for line, actual_line in zip(lines, transcript_entry.lines):
        assert line == actual_line
