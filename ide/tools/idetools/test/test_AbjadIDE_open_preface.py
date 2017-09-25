import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_open_preface_01():

    abjad_ide('red %letter po q')
    path = ide.Path('red_score', 'builds', 'letter', 'preface.pdf')
    transcript = abjad_ide.io.transcript
    assert f'Missing {path.trim()} ...' in transcript
