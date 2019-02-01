import abjad
import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


#@pytest.mark.skipif(
#    os.environ.get('TRAVIS') == 'true',
#    reason='Travis-CI does create LilyPond log.'
#    )
def test_AbjadIDE_edit_lilypond_log_01():

    abjad_ide('lp q')
    transcript = abjad_ide.io.transcript
    path = abjad.abjad_configuration.lilypond_log_file_path
    path = ide.Path(path)
    print('AAA', path)
    assert f'Editing {path.trim()} ...' in transcript


def test_AbjadIDE_edit_lilypond_log_02():
    """
    In external directory.
    """

    if not abjad_ide.test_baca_directories():
        return

    abjad_ide('cdk lp q')
    transcript = abjad_ide.io.transcript
    path = abjad.abjad_configuration.lilypond_log_file_path
    path = ide.Path(path)
    assert f'Editing {path.trim()} ...' in transcript
