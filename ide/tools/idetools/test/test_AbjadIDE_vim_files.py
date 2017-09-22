import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_vim_files_01():
    
    path = ide.Path('red_score').parent.parent.parent('etc', 'OPTIMIZATION')
    assert path.is_file()

    abjad_ide('red .. .. .. etc vi OPT q')
    transcript = abjad_ide.io.transcript
    assert f'Editing {path.trim()} ...' in transcript
