import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_dynamics_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score dcl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Activating 2 dynamic color tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score duc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Deactivating 2 dynamic color tags ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score dcl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Activating 2 dynamic color tags ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_dynamics_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ dcl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Skipping 2 (active) dynamic color tags ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ duc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Deactivating 2 dynamic color tags ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ dcl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring dynamics ...',
            ' Found 2 dynamic color tags ...',
            ' Activating 2 dynamic color tags ...',
            ]:
            assert line in lines
