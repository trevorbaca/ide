import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_clefs_01():
    r'''In build directory.
    '''

    with ide.Test():

        match = baca.tags.clef_color_match
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(match) == ((0, 0), (14, 14))
        
        abjad_ide('gre bb arch-a-score clc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((14, 14), (0, 0))
        for line in [
            'Found 14 clef color tags in arch-a-score ...',
            ' Activating 14 deactivated clef color tags in arch-a-score ...',
            ' No already-active clef color tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score bwc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((0, 0), (14, 14))
        for line in [
            'Found 14 clef color tags in arch-a-score ...',
            ' Deactivating 14 active clef color tags in arch-a-score ...',
            ' No already-deactivated clef color tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score clc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((14, 14), (0, 0))
        for line in [
            'Found 14 clef color tags in arch-a-score ...',
            ' Activating 14 deactivated clef color tags in arch-a-score ...',
            ' No already-active clef color tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_clefs_02():
    r'''In segment directory.
    '''

    with ide.Test():

        match = baca.tags.clef_color_match
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(match) == ((14, 14), (0, 0))
        
        abjad_ide('gre %_ clc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((14, 14), (0, 0))
        for line in [
            'Found 14 clef color tags in _ ...',
            ' No deactivated clef color tags to activate in _ ...',
            ' Skipping 14 already-active clef color tags in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ bwc q')
        assert path.count(match) == ((0, 0), (14, 14))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 14 clef color tags in _ ...',
            ' Deactivating 14 active clef color tags in _ ...',
            ' No already-deactivated clef color tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ clc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((14, 14), (0, 0))
        for line in [
            'Found 14 clef color tags in _ ...',
            ' Activating 14 deactivated clef color tags in _ ...',
            ' No already-active clef color tags to skip in _ ...',
            ]:
            assert line in lines
