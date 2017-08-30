import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_interpret_back_cover_01():

    with ide.Test():
        source = ide.PackagePath('red_score').builds / 'letter' / 'back-cover.tex'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %letter bci q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Interpreting back cover ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Interpreting back cover ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
