import ide
abjad_ide = ide.AbjadIDE(test=True)


#def test_AbjadIDE_trash_pdf_01():
#    r'''In material directory.
#    '''
#
#    with ide.Test():
#        target = ide.Path('red_score').materials('magic_numbers')
#        target /= 'illustration.pdf'
#
#        abjad_ide('red %magic pdfm q')
#        assert target.is_file()
#
#        abjad_ide('red %magic pdft q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not target.exists()
#
#
#def test_AbjadIDE_trash_pdf_02():
#    r'''In segment directory.
#    '''
#
#    with ide.Test():
#        target = ide.Path('red_score').segments('A')
#        target /= 'illustration.pdf'
#
#        abjad_ide('red %A pdfm q')
#        assert target.is_file()
#
#        abjad_ide('red %A pdft q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not target.exists()
