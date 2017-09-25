import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_front_cover_01():

    abjad_ide('red %letter fco q')
    path = ide.Path('red_score', 'builds', 'letter', 'front-cover.pdf')
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
