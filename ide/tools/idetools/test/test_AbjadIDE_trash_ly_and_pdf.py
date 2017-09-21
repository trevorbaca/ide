import ide
abjad_ide = ide.AbjadIDE(is_test=True)


#def test_AbjadIDE_trash_ly_and_pdf_01():
#    r'''In material directory.
#    '''
#
#    with ide.Test():
#        source = ide.Path('red_score').materials('magic_numbers')
#        source /= 'illustration.ly'
#        target = source.with_suffix('.pdf')
#
#        abjad_ide('red~score %magic pdfm q')
#        assert source.is_file()
#        assert target.is_file()
#
#        abjad_ide('red~score %magic trash q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {source.trim()} ...' in transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not source.exists()
#        assert not target.exists()
#
#
#def test_AbjadIDE_trash_ly_and_pdf_02():
#    r'''In segment directory.
#    '''
#
#    with ide.Test():
#        source = ide.Path('red_score').segments('segment_01')
#        source /= 'illustration.ly'
#        target = source.with_suffix('.pdf')
#
#        abjad_ide('red~score %A pdfm q')
#        assert source.is_file()
#        assert target.is_file()
#
#        abjad_ide('red~score %A trash q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {source.trim()} ...' in transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not source.exists()
#        assert not target.exists()
