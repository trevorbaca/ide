import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_edit_external_file_01():

    abjad_ide('red ww .gitignore o q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').wrapper('.gitignore')
    assert 'Open or edit (o|e)?> o' in transcript
    assert f'Opening {path.trim()} ...' in transcript

    abjad_ide('red ww .gitignore e q')
    transcript = abjad_ide.io.transcript
    path = ide.Path('red_score').wrapper('.gitignore')
    assert 'Open or edit (o|e)?> e' in transcript
    assert f'Editing {path.trim()} ...' in transcript
