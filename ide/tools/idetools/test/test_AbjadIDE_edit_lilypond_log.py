import abjad
import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Travis-CI does create LilyPond log.'
    )
def test_AbjadIDE_edit_lilypond_log_01():

    abjad_ide('lpg q')
    transcript = abjad_ide.io_manager.transcript
    path = abjad.abjad_configuration.lilypond_log_file_path
    assert f'Editing {path} ...' in transcript
