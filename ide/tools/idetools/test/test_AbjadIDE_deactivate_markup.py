import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_deactivate_markup_01():

    ly_paths = []
    for name in ('_', 'A', 'B'):
        ly_name = f'segment-{name}.ly'
        ly_path = ide.Path('red_score', 'builds', 'letter-score')
        ly_path = ly_path._segments(ly_name)
        ly_paths.append(ly_path)

    with ide.Test(remove=[ly_paths]):

        abjad_ide('red %let ctmx q')
        transcript = abjad_ide.io.transcript
        tag = abjad.tags.CLOCK_TIME_MARKUP
        assert f'No {tag} tags to deactivate in letter-score ...' in transcript


def test_AbjadIDE_deactivate_markup_02():

    abjad_ide('blu %let ctmx q')
    transcript = abjad_ide.io.transcript
    tag = abjad.tags.CLOCK_TIME_MARKUP
    assert f'No {tag} tags to deactivate in letter-score ...' in transcript
