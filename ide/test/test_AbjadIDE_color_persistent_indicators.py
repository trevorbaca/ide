import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_persistent_indicators_01():
    """
    In build directory.
    """

    with ide.Test():

        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build / '_segments' / 'segment--.ly'

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score picl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring persistent indicators ...',
            ' Found 26 persistent indicator color expression tags ...',
            ' Activating 26 persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Deactivating 1 persistent indicator color suppression tag ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score piuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring persistent indicators ...',
            ' Found 26 persistent indicator color expression tags ...',
            ' Deactivating 26 persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Activating 1 persistent indicator color suppression tag ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score picl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring persistent indicators ...',
            ' Found 26 persistent indicator color expression tags ...',
            ' Activating 26 persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Deactivating 1 persistent indicator color suppression tag ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_persistent_indicators_02():
    """
    In segment directory.
    """

    with ide.Test():

        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ picl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring persistent indicators ...',
            ' Found 30 persistent indicator color expression tags ...',
            ' Activating 4 persistent indicator color expression tags ...',
            ' Skipping 26 (active) persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Skipping 1 (inactive) persistent indicator color suppression tag ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ piuc q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Uncoloring persistent indicators ...',
            ' Found 26 persistent indicator color expression tags ...',
            ' Deactivating 26 persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Activating 1 persistent indicator color suppression tag ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ picl q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Coloring persistent indicators ...',
            ' Found 26 persistent indicator color expression tags ...',
            ' Activating 26 persistent indicator color expression tags ...',
            ' Found 1 persistent indicator color suppression tag ...',
            ' Deactivating 1 persistent indicator color suppression tag ...',
            ]:
            assert line in lines
