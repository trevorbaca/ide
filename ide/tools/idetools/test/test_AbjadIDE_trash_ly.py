import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_trash_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        target = ide.PackagePath('red_score')
        target = target / 'materials' / 'magic_numbers' / 'illustration.ly'
        assert target.is_file()

        input_ = 'red~score %magic~numbers lyt q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not target.exists()


def test_AbjadIDE_trash_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        target = ide.PackagePath('red_score')
        target = target / 'segments' / 'segment_01' / 'illustration.ly'
        assert target.is_file()

        input_ = 'red~score %A lyt q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not target.exists()
