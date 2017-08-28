import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_illustrate_file_01():

    with ide.Test():
        target = ide.Path('red_score').materials / 'magic_numbers'
        target /= '__illustrate__.py'
        target.remove()

        input_ = 'red~score %magic~numbers illm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript

        input_ = 'red~score %magic~numbers illm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()
        transcript = abjad_ide._io_manager._transcript.contents
        assert f'Preserving {abjad_ide._trim(target)} ...' in transcript
