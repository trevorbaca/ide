import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_git_push_01():
    """
    In score directories.
    """

    path = ide.Path('red_score')

    abjad_ide('red push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red bb push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red dd push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red ee push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red gg push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red gg A push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red mm push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red mm rpc push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red oo push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red tt push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript

    abjad_ide('red yy push q')
    transcript = abjad_ide.io.transcript
    assert 'Running git push ...' in transcript


def test_AbjadIDE_git_push_02():
    """
    In scores directory.
    """

    abjad_ide('push q')
    transcript = abjad_ide.io.transcript
    for path in [ide.Path('red_score'), ide.Path('blue_score')]:
        assert f'{path.wrapper} ...' in transcript
        assert 'Running git push ...' in transcript
