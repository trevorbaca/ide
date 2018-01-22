import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


tags = baca.tags.clef_color_tags

#def test_AbjadIDE_color_clefs_01():
#    r'''In build directory.
#    '''
#
#    with ide.Test():
#
#        build = ide.Path('green_score', 'builds', 'arch-a-score')
#        path = build('_segments', 'segment-_.ly')
#
#        abjad_ide('gre bb arch-a-score ggc q')
#        assert path.is_file()
#        assert path.count(tag) == ((0, 0), (2, 16))
#        
#        abjad_ide('gre bb arch-a-score ctm q')
#        lines = abjad_ide.io.transcript.lines
#        assert f'Activating 2 {tag} tags in arch-a-score ...' in lines
#        assert path.count(tag) == ((2, 16), (0, 0))
#
#        abjad_ide('gre bb arch-a-score ctmx q')
#        lines = abjad_ide.io.transcript.lines
#        assert f'Deactivating 2 {tag} tags in arch-a-score ...' in lines
#        assert path.count(tag) == ((0, 0), (2, 16))


#def test_AbjadIDE_color_clefs_02():
#    r'''In segment directory.
#    '''
#
#    with ide.Test():
#
#        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
#        assert path.is_file()
#        assert path.count(tag) == ((0, 0), (2, 16))
#        
#        abjad_ide('gre %_ clc q')
#        lines = abjad_ide.io.transcript.lines
#        assert f'No color clef tags to activate _ ...' in lines
#        assert path.count(tag) == ((2, 16), (0, 0))
#
#        abjad_ide('gre %_ ctmx q')
#        lines = abjad_ide.io.transcript.lines
#        assert f'Deactivating 2 {tag} tags in _ ...' in lines
#        assert path.count(tag) == ((0, 0), (2, 16))
