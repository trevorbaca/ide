import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_show_spacing_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score spms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing spacing markup ...',
            ' Found no spacing markup tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_show_spacing_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'layout.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ spms q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Showing spacing markup ...',
            ' Found 2 spacing markup tags ...',
            ' Activating 2 spacing markup tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ spmh q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Hiding spacing markup ...',
            ' Found 2 spacing markup tags ...',
            ' Deactivating 2 spacing markup tags ...',
            ]:
            assert line in lines
