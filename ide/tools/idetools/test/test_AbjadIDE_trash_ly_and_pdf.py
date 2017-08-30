import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_trash_ly_and_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').materials / 'magic_numbers'
        source /= 'illustration.ly'
        target = source.with_suffix('.pdf')

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert source.is_file()
        assert target.is_file()

        input_ = 'red~score %magic~numbers trash q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {source.trim()} ...' in abjad_ide._transcript
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not source.exists()
        assert not target.exists()


def test_AbjadIDE_trash_ly_and_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.PackagePath('red_score').segments / 'segment_01'
        source /= 'illustration.ly'
        target = source.with_suffix('.pdf')

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        assert source.is_file()
        assert target.is_file()

        input_ = 'red~score %A trash q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {source.trim()} ...' in abjad_ide._transcript
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not source.exists()
        assert not target.exists()
