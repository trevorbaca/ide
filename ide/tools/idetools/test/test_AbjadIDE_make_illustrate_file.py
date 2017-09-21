import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_illustrate_file_01():

    with ide.Test():
        target = ide.Path('red_score').materials('magic_numbers')
        target /= '__illustrate__.py'
        target.remove()

        abjad_ide('red~score %magic illm q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert f'Writing {target.trim()} ...' in transcript

        abjad_ide('red~score %magic illm q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        assert f'Preserving {target.trim()} ...' in transcript
