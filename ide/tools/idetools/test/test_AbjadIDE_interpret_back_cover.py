import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_interpret_back_cover_01():

    with ide.Test():
        source = ide.Path('red_score', 'builds', 'letter', 'back-cover.tex')
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red %letter bci q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting back cover ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red %letter bci q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting back cover ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
