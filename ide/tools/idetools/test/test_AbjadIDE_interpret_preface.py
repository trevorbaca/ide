import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_preface_01():

    with ide.Test():
        source = ide.Path('red_score').builds / 'letter' / 'preface.tex'
        target = source.with_suffix('.pdf')
        target.remove()

        abjad_ide('red~score %letter ri q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting preface ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        abjad_ide('red~score %letter ri q')
        transcript = abjad_ide.io.transcript
        assert 'Interpreting preface ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
