import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.CLOCK_TIME_MARKUP

def test_AbjadIDE_show_clock_time_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment--.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score ctms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing clock time markup ...',
            ' Found 2 clock time markup tags ...',
            ' Activating 2 clock time markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score ctmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding clock time markup ...',
            ' Found 2 clock time markup tags ...',
            ' Deactivating 2 clock time markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_clock_time_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ ctms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing clock time markup ...',
            ' Found 2 clock time markup tags ...',
            ' Activating 2 clock time markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ ctmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding clock time markup ...',
            ' Found 2 clock time markup tags ...',
            ' Deactivating 2 clock time markup tags ...',
            ]:
            assert line in lines
