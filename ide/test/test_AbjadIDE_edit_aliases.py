import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create aliases file.'
    )
def test_AbjadIDE_edit_aliases_01():

    abjad_ide('red mm metronome al q')
    transcript = abjad_ide.io.transcript
    path = ide.Path(abjad_ide.configuration.aliases_file_path)
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_aliases_02():
    """
    In external directory.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk al q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.configuration.aliases_file_path
    assert f'Editing {path.trim()} ...' in transcript
