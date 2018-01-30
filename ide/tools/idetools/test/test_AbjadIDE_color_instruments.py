import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_instruments_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')
        #match = baca.tags.instrument_color_match(path)

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        #assert path.count(match) == ((0, 0), (12, 12))
        
        abjad_ide('gre bb arch-a-score cli q')
        lines = abjad_ide.io.transcript.lines
        #assert path.count(match) == ((12, 12), (0, 0))
        for line in [
            'Found 12 instrument color tags in arch-a-score ...',
            ' Activating 12 deactivated instrument color tags in arch-a-score ...',
            ' No already-active instrument color tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score bwi q')
        lines = abjad_ide.io.transcript.lines
        #assert path.count(match) == ((0, 0), (12, 12))
        for line in [
            'Found 12 instrument color tags in arch-a-score ...',
            ' Deactivating 12 active instrument color tags in arch-a-score ...',
            ' No already-deactivated instrument color tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score cli q')
        lines = abjad_ide.io.transcript.lines
        #assert path.count(match) == ((12, 12), (0, 0))
        for line in [
            'Found 12 instrument color tags in arch-a-score ...',
            ' Activating 12 deactivated instrument color tags in arch-a-score ...',
            ' No already-active instrument color tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_instruments_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        #match = baca.tags.instrument_color_match(path)
        #assert path.count(match) == ((12, 12), (0, 0))
        
        abjad_ide('gre %_ cli q')
        lines = abjad_ide.io.transcript.lines
        #assert path.count(match) == ((12, 12), (0, 0))
        for line in [
            'Found 16 instrument color tags in _ ...',
            ' Activating 4 deactivated instrument color tags in _ ...',
            ' Skipping 12 already-active instrument color tags in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ bwi q')
        #assert path.count(match) == ((0, 0), (12, 12))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 12 instrument color tags in _ ...',
            ' Deactivating 12 active instrument color tags in _ ...',
            ' No already-deactivated instrument color tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ cli q')
        lines = abjad_ide.io.transcript.lines
        #assert path.count(match) == ((12, 12), (0, 0))
        for line in [
            'Found 12 instrument color tags in _ ...',
            ' Activating 12 deactivated instrument color tags in _ ...',
            ' No already-active instrument color tags to skip in _ ...',
            ]:
            assert line in lines
