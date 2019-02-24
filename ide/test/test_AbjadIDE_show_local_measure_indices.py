import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_local_measure_indices_01():
    """
    In build directory.
    """

    with ide.Test():

        tag = abjad.const.LOCAL_MEASURE_INDEX
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score lmis q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Activating 2 local measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score lmih q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Deactivating 2 local measure index markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_local_measure_indices_02():
    """
    In segment directory.
    """

    with ide.Test():

        tag = abjad.const.LOCAL_MEASURE_INDEX
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ lmis q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Activating 2 local measure index markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ lmih q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding local measure index markup ...',
            ' Found 2 local measure index markup tags ...',
            ' Deactivating 2 local measure index markup tags ...',
            ]:
            assert line in lines
