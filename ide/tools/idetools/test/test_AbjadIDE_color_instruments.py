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

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score icl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring instruments ...',
            ' Activating instrument color tags in arch-a-score ...',
            '  Found 12 instrument color tags in arch-a-score ...',
            '  Activating 12 instrument color tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score iuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring instruments ...',
            ' Deactivating instrument color tags in arch-a-score ...',
            '  Found 12 instrument color tags in arch-a-score ...',
            '  Deactivating 12 instrument color tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score icl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring instruments ...',
            ' Activating instrument color tags in arch-a-score ...',
            '  Found 12 instrument color tags in arch-a-score ...',
            '  Activating 12 instrument color tags in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_instruments_02():
    r'''In segment directory.
    '''

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ icl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring instruments ...',
            ' Activating instrument color tags in _ ...',
            '  Found 16 instrument color tags in _ ...',
            '  Activating 4 instrument color tags in _ ...',
            '  Skipping 12 (active) instrument color tags in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ iuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring instruments ...',
            ' Deactivating instrument color tags in _ ...',
            '  Found 12 instrument color tags in _ ...',
            '  Deactivating 12 instrument color tags in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ icl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring instruments ...',
            ' Activating instrument color tags in _ ...',
            '  Found 12 instrument color tags in _ ...',
            '  Activating 12 instrument color tags in _ ...',
            ]:
            assert line in lines
