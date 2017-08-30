import ide
import os
import pytest
import shutil
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_interpret_score_01():

    with ide.Test():
        source = ide.PackagePath('red_score').builds / 'letter' / 'score.tex'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %letter fci pi mi bci si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Interpreting score ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        input_ = 'red~score bb letter fci pi mi bci si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
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
        pdf = ide.PackagePath('red_score').builds / 'letter' / 'front-cover.pdf'
        pdf.remove()
        input_ = 'red~score %letter si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'ERROR IN LATEX LOG FILE ...' in transcript
