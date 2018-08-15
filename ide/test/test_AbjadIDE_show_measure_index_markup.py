import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_measure_index_markup_01():
    """
    In build directory.
    """

    with ide.Test():

        tag = abjad.tags.MEASURE_INDEX_MARKUP
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score mims q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing measure index markup ...',
            ' Found 2 measure index markup tags ...',
            ' Activating 2 measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score mimh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding measure index markup ...',
            ' Found 2 measure index markup tags ...',
            ' Deactivating 2 measure index markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_measure_index_markup_02():
    """
    In segment directory.
    """

    with ide.Test():

        tag = abjad.tags.MEASURE_INDEX_MARKUP
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ mims q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing measure index markup ...',
            ' Found 2 measure index markup tags ...',
            ' Activating 2 measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ mimh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding measure index markup ...',
            ' Found 2 measure index markup tags ...',
            ' Deactivating 2 measure index markup tags ...',
            ]:
            assert line in lines
