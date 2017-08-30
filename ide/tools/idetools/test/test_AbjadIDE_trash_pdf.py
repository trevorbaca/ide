import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_trash_pdf_01():
    r'''In material directory.
    '''

    with ide.Test():
        target = ide.PackagePath('red_score').materials / 'magic_numbers'
        target /= 'illustration.pdf'

        input_ = 'red~score %magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()

        input_ = 'red~score %magic~numbers pdft q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not target.exists()


def test_AbjadIDE_trash_pdf_02():
    r'''In segment directory.
    '''

    with ide.Test():
        target = ide.PackagePath('red_score').segments / 'segment_01'
        target /= 'illustration.pdf'

        input_ = 'red~score %A pdfm q'
        abjad_ide._start(input_=input_)
        assert target.is_file()

        input_ = 'red~score %A pdft q'
        abjad_ide._start(input_=input_)
        assert f'Trashing {target.trim()} ...' in abjad_ide._transcript
        assert not target.exists()
