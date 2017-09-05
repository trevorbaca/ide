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
    transcript = abjad_ide.io_manager.transcript
    path = abjad_ide.io_manager.configuration.latex_log_file_path
    assert f'Editing {path} ...' in transcript
