import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create LaTeX log.'
    )
def test_AbjadIDE_edit_latex_log_01():

    path = abjad_ide._configuration.latex_log_file_path

    input_ = 'lxg q'
    abjad_ide._start(input_=input_)
    assert f'Editing {path} ...' in abjad_ide._transcript
