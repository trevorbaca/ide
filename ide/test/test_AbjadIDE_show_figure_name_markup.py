import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.FIGURE_NAME_MARKUP

def test_AbjadIDE_show_figure_name_markup_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment--.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score fnms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing figure name markup ...',
            ' Found 1 figure name markup tag ...',
            ' Activating 1 figure name markup tag ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score fnmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding figure name markup ...',
            ' Found 1 figure name markup tag ...',
            ' Deactivating 1 figure name markup tag ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_figure_name_markup_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ fnmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding figure name markup ...',
            ' Found 1 figure name markup tag ...',
            ' Deactivating 1 figure name markup tag ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ fnms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing figure name markup ...',
            ' Found 1 figure name markup tag ...',
            ' Activating 1 figure name markup tag ...',
            ]:
            assert line in lines
