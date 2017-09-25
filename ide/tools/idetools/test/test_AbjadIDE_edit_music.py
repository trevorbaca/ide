import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_music_01():
    
    abjad_ide('red %letter me q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score', 'builds', 'letter', 'music.ly')
    assert f'Editing {path.trim()} ...' in transcript
