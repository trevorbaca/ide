import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_dynamics_01():
    r'''In build directory.
    '''

    with ide.Test():

        match = baca.tags.dynamic_color_match
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(match) == ((0, 0), (2, 2))
        
        abjad_ide('gre bb arch-a-score dcl q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((2, 2), (0, 0))
        for line in [
            'Coloring dynamics ...',
            ' Activating color dynamic tags in arch-a-score ...',
            '  Found 2 color dynamic tags in arch-a-score ...',
            '  Activating 2 color dynamic tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score duc q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((0, 0), (2, 2))
        for line in [
            'Uncoloring dynamics ...',
            ' Deactivating dynamic tags in arch-a-score ...',
            '  Found 2 dynamic tags in arch-a-score ...',
            '  Deactivating 2 dynamic tags in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score dcl q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((2, 2), (0, 0))
        for line in [
            'Coloring dynamics ...',
            ' Activating color dynamic tags in arch-a-score ...',
            '  Found 2 color dynamic tags in arch-a-score ...',
            '  Activating 2 color dynamic tags in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_dynamics_02():
    r'''In segment directory.
    '''

    with ide.Test():

        match = baca.tags.dynamic_color_match
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(match) == ((2, 2), (0, 0))
        
        abjad_ide('gre %_ dcl q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((2, 2), (0, 0))
        for line in [
            'Coloring dynamics ...',
            ' Activating color dynamic tags in _ ...',
            '  Found 2 color dynamic tags in _ ...',
            '  Skipping 2 (active) color dynamic tags in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ duc q')
        assert path.count(match) == ((0, 0), (2, 2))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring dynamics ...',
            ' Deactivating dynamic tags in _ ...',
            '  Found 2 dynamic tags in _ ...',
            '  Deactivating 2 dynamic tags in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ dcl q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(match) == ((2, 2), (0, 0))
        for line in [
            'Coloring dynamics ...',
            ' Activating color dynamic tags in _ ...',
            '  Found 2 color dynamic tags in _ ...',
            '  Activating 2 color dynamic tags in _ ...',
            ]:
            assert line in lines
