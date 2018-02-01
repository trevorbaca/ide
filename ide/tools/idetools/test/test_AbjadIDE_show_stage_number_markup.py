import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


tag = abjad.tags.STAGE_NUMBER_MARKUP

def test_AbjadIDE_show_stage_number_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score snms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing stage number markup ...',
            ' Found 2 stage number markup tags in arch-a-score ...',
            ' Activating 2 stage number markup tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score snmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding stage number markup ...',
            ' Found 2 stage number markup tags in arch-a-score ...',
            ' Deactivating 2 stage number markup tags in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_stage_number_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ snms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing stage number markup ...',
            ' Found 2 stage number markup tags in _ ...',
            ' Activating 2 stage number markup tags in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ snmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding stage number markup ...',
            ' Found 2 stage number markup tags in _ ...',
            ' Deactivating 2 stage number markup tags in _ ...',
            ]:
            assert line in lines
