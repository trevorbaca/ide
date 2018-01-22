import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_activate_markup_01():
    r'''CLOCK_TIME_MARKUP.
    '''

    # segment directory
    with ide.Test():

        segment = ide.Path('green_score', 'segments', '_')
        illustration_ly = segment('illustration.ly')
        assert illustration_ly.is_file()

        tag = abjad.tags.CLOCK_TIME_MARKUP
        assert illustration_ly.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre %_ ctm q')
        lines = abjad_ide.io.transcript.lines
        assert f'Activating 2 {tag} tags in _ ...' in lines
        assert illustration_ly.count(tag) == ((2, 16), (0, 0))

        abjad_ide('gre %_ ctmx q')
        lines = abjad_ide.io.transcript.lines
        assert f'Deactivating 2 {tag} tags in _ ...' in lines
        assert illustration_ly.count(tag) == ((0, 0), (2, 16))


#def test_AbjadIDE_activate_markup_02():
#    r'''In build directory.
#    '''
#
#    pass
