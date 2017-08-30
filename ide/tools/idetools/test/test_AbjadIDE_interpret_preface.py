import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_preface_01():

    with ide.Test():
        source = ide.PackagePath('red_score').builds / 'letter' / 'preface.tex'
        target = source.with_suffix('.pdf')
        target.remove()

        input_ = 'red~score %letter pi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Interpreting preface ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()

        input_ = 'red~score %letter pi q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Interpreting preface ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' in transcript
        assert target.is_file()
