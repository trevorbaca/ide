import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_back_cover_01():

    abjad_ide('red %letter bco q')
    path = ide.Path('red_score', 'builds', 'letter-score', 'back-cover.pdf')
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
