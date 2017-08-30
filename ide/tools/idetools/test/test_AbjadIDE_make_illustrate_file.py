import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_illustrate_file_01():

    with ide.Test():
        target = ide.PackagePath('red_score').materials / 'magic_numbers'
        target /= '__illustrate__.py'
        target.remove()

        input_ = 'red~score %magic~numbers illm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        transcript = abjad_ide._transcript
        assert f'Writing {target.trim()} ...' in transcript

        input_ = 'red~score %magic~numbers illm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        transcript = abjad_ide._transcript
        assert f'Preserving {target.trim()} ...' in transcript
