import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_local_measure_index_markup_01():
    """
    In build directory.
    """

    with ide.Test():

        tag = abjad.tags.LOCAL_MEASURE_INDEX_MARKUP
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score lmims q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Activating 2 local measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score lmimh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Deactivating 2 local measure index markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_local_measure_index_markup_02():
    """
    In segment directory.
    """

    with ide.Test():

        tag = abjad.tags.LOCAL_MEASURE_INDEX_MARKUP
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ lmims q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Activating 2 local measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ lmimh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Deactivating 2 local measure index markup tags ...',
            ]:
            assert line in lines
