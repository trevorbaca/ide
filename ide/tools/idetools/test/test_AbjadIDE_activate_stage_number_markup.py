import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.STAGE_NUMBER_MARKUP

def test_AbjadIDE_activate_stage_number_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre bb arch-a-score snm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((2, 16), (0, 0))
        for line in [
            'Found 2 STAGE_NUMBER_MARKUP tags in arch-a-score ...',
            ' Activating 2 deactivated STAGE_NUMBER_MARKUP tags in arch-a-score ...',
            ' No already-active STAGE_NUMBER_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score snmx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 STAGE_NUMBER_MARKUP tags in arch-a-score ...',
            ' Deactivating 2 active STAGE_NUMBER_MARKUP tags in arch-a-score ...',
            ' No already-deactivated STAGE_NUMBER_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_activate_stage_number_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre %_ snm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((2, 16), (0, 0))
        for line in [
            'Found 2 STAGE_NUMBER_MARKUP tags in _ ...',
            ' Activating 2 deactivated STAGE_NUMBER_MARKUP tags in _ ...',
            ' No already-active STAGE_NUMBER_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ snmx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 STAGE_NUMBER_MARKUP tags in _ ...',
            ' Deactivating 2 active STAGE_NUMBER_MARKUP tags in _ ...',
            ' No already-deactivated STAGE_NUMBER_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines
