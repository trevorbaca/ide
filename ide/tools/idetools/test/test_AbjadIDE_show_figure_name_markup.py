import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.FIGURE_NAME_MARKUP

def test_AbjadIDE_show_figure_name_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (1, 4))
        
        abjad_ide('gre bb arch-a-score fnms q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((1, 4), (0, 0))
        for line in [
            'Activating FIGURE_NAME_MARKUP tags in arch-a-score ...',
            ' Found 1 FIGURE_NAME_MARKUP tag in arch-a-score ...',
            ' Activating 1 FIGURE_NAME_MARKUP tag in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score fnmh q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (1, 4))
        for line in [
            'Deactivating FIGURE_NAME_MARKUP tags in arch-a-score ...',
            ' Found 1 FIGURE_NAME_MARKUP tag in arch-a-score ...',
            ' Deactivating 1 FIGURE_NAME_MARKUP tag in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_figure_name_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(tag) == ((1, 4), (0, 0))
        
        abjad_ide('gre %_ fnmh q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (1, 4))
        for line in [
            'Deactivating FIGURE_NAME_MARKUP tags in _ ...',
            ' Found 1 FIGURE_NAME_MARKUP tag in _ ...',
            ' Deactivating 1 FIGURE_NAME_MARKUP tag in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ fnms q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((1, 4), (0, 0))
        for line in [
            'Activating FIGURE_NAME_MARKUP tags in _ ...',
            ' Found 1 FIGURE_NAME_MARKUP tag in _ ...',
            ' Activating 1 FIGURE_NAME_MARKUP tag in _ ...',
            ]:
            assert line in lines
