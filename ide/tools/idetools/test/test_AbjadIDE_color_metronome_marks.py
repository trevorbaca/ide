import abjad
import baca
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_color_metronome_marks_01():
    r'''In build directory.
    '''

    with ide.Test():

        expression = baca.tags.metronome_mark_color_expression_match
        suppression = baca.tags.metronome_mark_color_suppression_match
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(expression) == ((0, 0), (1, 23))
        assert path.count(suppression) == ((1, 19), (0, 0))
        
        abjad_ide('gre bb arch-a-score cltm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(expression) == ((1, 23), (0, 0))
        assert path.count(suppression) == ((0, 0), (1, 19))
        for line in [
            'Found 1 metronome mark color expression tag in arch-a-score ...',
            ' Activating 1 deactivated metronome mark color expression tag in arch-a-score ...',
            ' No already-active metronome mark color expression tags to skip in arch-a-score ...',
            'Found 1 metronome mark color suppression tag in arch-a-score ...',
            ' Deactivating 1 active metronome mark color suppression tag in arch-a-score ...',
            ' No already-deactivated metronome mark color suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score bwtm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(expression) == ((0, 0), (1, 23))
        assert path.count(suppression) == ((1, 19), (0, 0))
        for line in [
            'Found 1 b&w metronome mark expression tag in arch-a-score ...',
            ' Activating 1 deactivated b&w metronome mark expression tag in arch-a-score ...',
            ' No already-active b&w metronome mark expression tags to skip in arch-a-score ...',
            'Found 1 b&w metronome mark suppression tag in arch-a-score ...',
            ' Deactivating 1 active b&w metronome mark suppression tag in arch-a-score ...',
            ' No already-deactivated b&w metronome mark suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score cltm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(expression) == ((1, 23), (0, 0))
        assert path.count(suppression) == ((0, 0), (1, 19))
        for line in [
            'Found 1 metronome mark color expression tag in arch-a-score ...',
            ' Activating 1 deactivated metronome mark color expression tag in arch-a-score ...',
            ' No already-active metronome mark color expression tags to skip in arch-a-score ...',
            'Found 1 metronome mark color suppression tag in arch-a-score ...',
            ' Deactivating 1 active metronome mark color suppression tag in arch-a-score ...',
            ' No already-deactivated metronome mark color suppression tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_color_metronome_marks_02():
    r'''In segment directory.
    '''

    with ide.Test():

        expression = baca.tags.metronome_mark_color_expression_match
        suppression = baca.tags.metronome_mark_color_suppression_match
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(expression) == ((1, 23), (0, 0))
        assert path.count(suppression) == ((0, 0), (1, 19))
        
        abjad_ide('gre %_ cltm q')
        assert path.count(expression) == ((1, 23), (0, 0))
        assert path.count(suppression) == ((0, 0), (1, 19))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 1 metronome mark color expression tag in _ ...',
            ' No deactivated metronome mark color expression tags to activate in _ ...',
            ' Skipping 1 already-active metronome mark color expression tag in _ ...',
            'Found 1 metronome mark color suppression tag in _ ...',
            ' No active metronome mark color suppression tags to deactivate in _ ...',
            ' Skipping 1 already-deactivated metronome mark color suppression tag in _ ...',
            ]:
            assert line in lines
        
        abjad_ide('gre %_ bwtm q')
        assert path.count(expression) == ((0, 0), (1, 23))
        assert path.count(suppression) == ((1, 19), (0, 0))
        lines = abjad_ide.io.transcript.lines
        for line in [
            'Found 1 b&w metronome mark expression tag in _ ...',
            ' Activating 1 deactivated b&w metronome mark expression tag in _ ...',
            ' No already-active b&w metronome mark expression tags to skip in _ ...',
            'Found 1 b&w metronome mark suppression tag in _ ...',
            ' Deactivating 1 active b&w metronome mark suppression tag in _ ...',
            ' No already-deactivated b&w metronome mark suppression tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ cltm q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(expression) == ((1, 23), (0, 0))
        assert path.count(suppression) == ((0, 0), (1, 19))
        for line in [
            'Found 1 metronome mark color expression tag in _ ...',
            ' Activating 1 deactivated metronome mark color expression tag in _ ...',
            ' No already-active metronome mark color expression tags to skip in _ ...',
            'Found 1 metronome mark color suppression tag in _ ...',
            ' Deactivating 1 active metronome mark color suppression tag in _ ...',
            ' No already-deactivated metronome mark color suppression tags to skip in _ ...',
            ]:
            assert line in lines
