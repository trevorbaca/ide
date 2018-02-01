import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_clefs_01():
    r'''In build directory.
    '''

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score ccl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring clefs ...',
            ' Activating clef color tags in arch-a-score ...',
            '  Found 14 clef color tags in arch-a-score ...',
            '  Activating 14 clef color tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score cuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring clefs ...',
            ' Deactivating clef color tags in arch-a-score ...',
            '  Found 14 clef color tags in arch-a-score ...',
            '  Deactivating 14 clef color tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score ccl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring clefs ...',
            ' Activating clef color tags in arch-a-score ...',
            '  Found 14 clef color tags in arch-a-score ...',
            '  Activating 14 clef color tags in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_clefs_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ ccl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring clefs ...',
            ' Activating clef color tags in _ ...',
            '  Found 14 clef color tags in _ ...',
            '  Skipping 14 (active) clef color tags in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ cuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring clefs ...',
            ' Deactivating clef color tags in _ ...',
            '  Found 14 clef color tags in _ ...',
            '  Deactivating 14 clef color tags in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ ccl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring clefs ...',
            ' Activating clef color tags in _ ...',
            '  Found 14 clef color tags in _ ...',
            '  Activating 14 clef color tags in _ ...',
            ]:
            assert line in lines
