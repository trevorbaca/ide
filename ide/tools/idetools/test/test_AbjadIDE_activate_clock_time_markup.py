import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.CLOCK_TIME_MARKUP

def test_AbjadIDE_activate_clock_time_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre bb arch-a-score ctm q')
        assert path.count(tag) == ((2, 16), (0, 0))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 2 CLOCK_TIME_MARKUP tags in arch-a-score ...',
            ' Activating 2 deactivated CLOCK_TIME_MARKUP tags in arch-a-score ...',
            ' No already-active CLOCK_TIME_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score ctmx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 CLOCK_TIME_MARKUP tags in arch-a-score ...',
            ' Deactivating 2 active CLOCK_TIME_MARKUP tags in arch-a-score ...',
            ' No already-deactivated CLOCK_TIME_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_activate_clock_time_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre %_ ctm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((2, 16), (0, 0))
        for line in [
            'Found 2 CLOCK_TIME_MARKUP tags in _ ...',
            ' Activating 2 deactivated CLOCK_TIME_MARKUP tags in _ ...',
            ' No already-active CLOCK_TIME_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ ctmx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 CLOCK_TIME_MARKUP tags in _ ...',
            ' Deactivating 2 active CLOCK_TIME_MARKUP tags in _ ...',
            ' No already-deactivated CLOCK_TIME_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines
