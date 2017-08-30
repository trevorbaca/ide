import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create aliases file.'
    )
def test_AbjadIDE_edit_aliases_file_01():

    path = abjad_ide._configuration.aliases_file_path

    input_ = 'red~score mm tempi als q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path} ...' in abjad_ide._transcript
