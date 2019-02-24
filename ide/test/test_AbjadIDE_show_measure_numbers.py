import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_measure_numbers_01():
    """
    In build directory.
    """

    with ide.Test():

        tag = abjad.const.MEASURE_NUMBER_MARKUP
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score mns q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing measure number markup ...',
            ' Found 2 measure number markup tags ...',
            ' Activating 2 measure number markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score mnh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding measure number markup ...',
            ' Found 2 measure number markup tags ...',
            ' Deactivating 2 measure number markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_measure_numbers_02():
    """
    In segment directory.
    """

    with ide.Test():

        tag = abjad.const.MEASURE_NUMBER_MARKUP
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ mns q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing measure number markup ...',
            ' Found 2 measure number markup tags ...',
            ' Activating 2 measure number markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ mnh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding measure number markup ...',
            ' Found 2 measure number markup tags ...',
            ' Deactivating 2 measure number markup tags ...',
            ]:
            assert line in lines
