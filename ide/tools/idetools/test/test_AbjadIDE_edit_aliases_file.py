import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create aliases file.'
    )
def test_AbjadIDE_edit_aliases_file_01():

    abjad_ide('red~score mm tempi als q')
    transcript = abjad_ide.io_manager.transcript
    path = abjad_ide.io_manager.configuration.aliases_file_path
    assert f'Editing {path} ...' in transcript
