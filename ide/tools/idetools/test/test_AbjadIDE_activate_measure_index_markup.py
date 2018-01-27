import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_activate_measure_index_markup_01():
    r'''In build directory.
    '''

    with ide.Test():

        tag = abjad.tags.MEASURE_INDEX_MARKUP
        build = ide.Path('green_score', 'builds', 'arch-a-score')
        path = build('_segments', 'segment-_.ly')

        abjad_ide('gre bb arch-a-score ggc q')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre bb arch-a-score mim q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((2, 16), (0, 0))
        for line in [
            'Found 2 MEASURE_INDEX_MARKUP tags in arch-a-score ...',
            ' Activating 2 deactivated MEASURE_INDEX_MARKUP tags in arch-a-score ...',
            ' No already-active MEASURE_INDEX_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines

        abjad_ide('gre bb arch-a-score mimx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 MEASURE_INDEX_MARKUP tags in arch-a-score ...',
            ' Deactivating 2 active MEASURE_INDEX_MARKUP tags in arch-a-score ...',
            ' No already-deactivated MEASURE_INDEX_MARKUP tags to skip in arch-a-score ...',
            ]:
            assert line in lines


def test_AbjadIDE_activate_measure_index_markup_02():
    r'''In segment directory.
    '''

    with ide.Test():

        tag = abjad.tags.MEASURE_INDEX_MARKUP
        path = ide.Path('green_score', 'segments', '_', 'illustration.ly')
        assert path.is_file()
        assert path.count(tag) == ((0, 0), (2, 16))
        
        abjad_ide('gre %_ mim q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((2, 16), (0, 0))
        for line in [
            'Found 2 MEASURE_INDEX_MARKUP tags in _ ...',
            ' Activating 2 deactivated MEASURE_INDEX_MARKUP tags in _ ...',
            ' No already-active MEASURE_INDEX_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines

        abjad_ide('gre %_ mimx q')
        lines = abjad_ide.io.transcript.lines
        assert path.count(tag) == ((0, 0), (2, 16))
        for line in [
            'Found 2 MEASURE_INDEX_MARKUP tags in _ ...',
            ' Deactivating 2 active MEASURE_INDEX_MARKUP tags in _ ...',
            ' No already-deactivated MEASURE_INDEX_MARKUP tags to skip in _ ...',
            ]:
            assert line in lines
