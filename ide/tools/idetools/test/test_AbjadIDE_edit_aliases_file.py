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
    transcript = abjad_ide.io.transcript
    path = abjad_ide.configuration.aliases_file_path
    assert f'Editing {path} ...' in transcript


def test_AbjadIDE_edit_aliases_file_02():
    r'''In external directory.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdk als q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.configuration.aliases_file_path
    assert f'Editing {path} ...' in transcript
