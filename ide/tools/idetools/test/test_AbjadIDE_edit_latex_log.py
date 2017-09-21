import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create LaTeX log.'
    )
def test_AbjadIDE_edit_latex_log_01():

    abjad_ide('lx q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.configuration.latex_log_file_path
    assert f'Editing {path} ...' in transcript


def test_AbjadIDE_edit_latex_log_02():
    r'''In external directory.
    '''

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk lx q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.configuration.latex_log_file_path
    assert f'Editing {path} ...' in transcript
