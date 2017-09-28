import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_illustrate_01():

    with ide.Test():
        target = ide.Path(
            'red_score', 'materials', 'red_pitch_classes', '__illustrate__.py')
        target.remove()

        abjad_ide('red %rpc illm q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert f'Writing {target.trim()} ...' in transcript

        abjad_ide('red %rpc illm q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert f'Preserving {target.trim()} ...' in transcript
