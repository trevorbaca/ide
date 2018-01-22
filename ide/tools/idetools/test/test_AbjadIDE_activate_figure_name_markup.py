import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.FIGURE_NAME_MARKUP

def test_AbjadIDE_activate_figure_name_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (1, 4))
        
        abjad_ide('gre bb arch-a-score fnm q')
        lines = abjad_ide.io.transcript.lines
        assert f'Activating 1 {tag} tag in arch-a-score ...' in lines
        assert path.count(tag) == ((1, 4), (0, 0))

        abjad_ide('gre bb arch-a-score fnmx q')
        lines = abjad_ide.io.transcript.lines
        assert f'Deactivating 1 {tag} tag in arch-a-score ...' in lines
        assert path.count(tag) == ((0, 0), (1, 4))


def test_AbjadIDE_activate_figure_name_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(tag) == ((1, 4), (0, 0))
        
        abjad_ide('gre %_ fnmx q')
        lines = abjad_ide.io.transcript.lines
        assert f'Deactivating 1 {tag} tag in _ ...' in lines
        assert path.count(tag) == ((0, 0), (1, 4))

        abjad_ide('gre %_ fnm q')
        lines = abjad_ide.io.transcript.lines
        assert f'Activating 1 {tag} tag in _ ...' in lines
        assert path.count(tag) == ((1, 4), (0, 0))
