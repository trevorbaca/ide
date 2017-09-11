import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create LaTeX log.'
    )
def test_AbjadIDE_edit_latex_log_01():

    abjad_ide('lxg q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.io.configuration.latex_log_file_path
    assert f'Editing {path} ...' in transcript


def test_AbjadIDE_edit_latex_log_02():
    r'''In external directory.
    '''

    if not abjad_ide._test_external_directory():
        return

    abjad_ide('cdk lxg q')
    transcript = abjad_ide.io.transcript
    path = abjad_ide.io.configuration.latex_log_file_path
    assert f'Editing {path} ...' in transcript
