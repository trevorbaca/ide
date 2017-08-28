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
        source = ide.Path('red_score') / 'build' / 'letter' / 'score.tex'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %letter fci pi mi bci si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting score ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()

        input_ = 'red~score bb letter fci pi mi bci si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Interpreting score ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Interpreting {abjad_ide._trim(source)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert f'Opening {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()


def test_AbjadIDE_interpret_score_02():
    r'''LaTeX error does not freeze IDE.
    '''

    with ide.Test():
        pdf = ide.Path('red_score').build / 'letter' / 'front-cover.pdf'
        pdf.remove()
        input_ = 'red~score %letter si q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'ERROR IN LATEX LOG FILE ...' in transcript
