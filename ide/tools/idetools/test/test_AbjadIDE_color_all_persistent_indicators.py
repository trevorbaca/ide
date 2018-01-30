import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_all_persistent_indicators_01():
    r'''In build directory.
    '''

    with ide.Test():

        match = baca.tags.clef_color_match
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        
        abjad_ide('gre bb arch-a-score cl* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 26 persistent indicator color expression tags in arch-a-score ...',
            ' Activating 26 deactivated persistent indicator color expression tags in arch-a-score ...',
            ' No already-active persistent indicator color expression tags to skip in arch-a-score ...',
            'Found 1 persistent indicator color suppression tag in arch-a-score ...',
            ' Deactivating 1 active persistent indicator color suppression tag in arch-a-score ...',
            ' No already-deactivated persistent indicator color suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score bw* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 26 persistent indicator color expression tags in arch-a-score ...',
            ' Deactivating 26 active persistent indicator color expression tags in arch-a-score ...',
            ' No already-deactivated persistent indicator color expression tags to skip in arch-a-score ...',
            'Found 1 persistent indicator color suppression tag in arch-a-score ...',
            ' Activating 1 deactivated persistent indicator color suppression tag in arch-a-score ...',
            ' No already-active persistent indicator color suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score cl* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 26 persistent indicator color expression tags in arch-a-score ...',
            ' Activating 26 deactivated persistent indicator color expression tags in arch-a-score ...',
            ' No already-active persistent indicator color expression tags to skip in arch-a-score ...',
            'Found 1 persistent indicator color suppression tag in arch-a-score ...',
            ' Deactivating 1 active persistent indicator color suppression tag in arch-a-score ...',
            ' No already-deactivated persistent indicator color suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_all_persistent_indicators_02():
    r'''In segment directory.
    '''

    with ide.Test():

        match = baca.tags.clef_color_match
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        
        abjad_ide('gre %_ cl* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 30 persistent indicator color expression tags in _ ...',
            ' Activating 4 deactivated persistent indicator color expression tags in _ ...',
            ' Skipping 26 already-active persistent indicator color expression tags in _ ...',
            'Found 1 persistent indicator color suppression tag in _ ...',
            #' No active persistent indicator color suppression tags to deactivate in _ ...'
            ' Skipping 1 already-deactivated persistent indicator color suppression tag in _ ...'
            ]:
            assert line in lines
        
        abjad_ide('gre %_ bw* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 26 persistent indicator color expression tags in _ ...',
            ' Deactivating 26 active persistent indicator color expression tags in _ ...',
            ' No already-deactivated persistent indicator color expression tags to skip in _ ...',
            'Found 1 persistent indicator color suppression tag in _ ...',
            ' Activating 1 deactivated persistent indicator color suppression tag in _ ...',
            ' No already-active persistent indicator color suppression tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ cl* q')
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 26 persistent indicator color expression tags in _ ...',
            ' Activating 26 deactivated persistent indicator color expression tags in _ ...',
            ' No already-active persistent indicator color expression tags to skip in _ ...',
            'Found 1 persistent indicator color suppression tag in _ ...',
            ' Deactivating 1 active persistent indicator color suppression tag in _ ...',
            ' No already-deactivated persistent indicator color suppression tags to skip in _ ...',
            ]:
            assert line in lines
