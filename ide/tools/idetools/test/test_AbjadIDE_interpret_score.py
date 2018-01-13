import ide
import os
import pytest
import shutil
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_interpret_score_01():

    with ide.Test():
        source = ide.Path('red_score', 'builds', 'letter-score', 'score.tex')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %letter fci pi mi bci ri q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting score ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red bb letter fci pi mi bci ri q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting score ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()


def test_AbjadIDE_interpret_score_02():
    r'''LaTeX error does not freeze IDE.
    '''

    with ide.Test():
        pdf = ide.Path('red_score', 'builds', 'letter-score', 'front-cover.pdf')
        pdf.remove()

        abjad_ide('red %letter ri q')
        transcript = abjad_ide.io.transcript
        assert 'ERROR IN LATEX LOG FILE ...' in transcript
