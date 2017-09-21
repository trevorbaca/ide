import ide
abjad_ide = ide.AbjadIDE(test=True)


#def test_AbjadIDE_trash_ly_01():
#    r'''In material directory.
#    '''
#
#    with ide.Test():
#        target = ide.Path('red_score')
#        target = target / 'materials' / 'magic_numbers' / 'illustration.ly'
#        assert target.is_file()
#
#        abjad_ide('red~score %magic lyt q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not target.exists()
#
#
#def test_AbjadIDE_trash_ly_02():
#    r'''In segment directory.
#    '''
#
#    with ide.Test():
#        target = ide.Path('red_score')
#        target = target / 'segments' / 'segment_01' / 'illustration.ly'
#        assert target.is_file()
#
#        abjad_ide('red~score %A lyt q')
#        transcript = abjad_ide.io.transcript
#        assert f'Trashing {target.trim()} ...' in transcript
#        assert not target.exists()
