import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_ly_01():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials()
        source = source / 'magic_numbers' / '__illustrate__.py'
        target = source.with_name('illustration.ly')
        target.remove()

        abjad_ide('red~score %magic lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()

        abjad_ide('red~score %magic lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()


def test_AbjadIDE_make_ly_02():
    r'''In segment directory.
    '''

    with ide.Test():
        target = ide.Path('red_score').segments('A')
        target /= 'illustration.ly'
        illustrate = target.with_name('__illustrate__.py')
        target.remove()

        abjad_ide('red~score %A lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()

        abjad_ide('red~score %A lym q')
        transcript = abjad_ide.io.transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()
