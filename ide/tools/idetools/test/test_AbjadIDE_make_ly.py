import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_make_ly_01():
    r'''In material directory.
    '''

    source = ide.PackagePath('red_score').materials
    source = source / 'magic_numbers' / '__illustrate__.py'
    target = source.with_name('illustration.ly')
    with ide.Test(keep=[target]):
        target.remove()

        input_ = 'red~score %magic~numbers lym q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)

        input_ = 'red~score %magic~numbers lym q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Interpreting {source.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)


def test_AbjadIDE_make_ly_02():
    r'''In segment directory.
    '''

    target = ide.PackagePath('red_score').segments / 'segment_01' / 'illustration.ly'
    with ide.Test(keep=[target]):
        illustrate = target.with_name('__illustrate__.py')
        target.remove()

        input_ = 'red~score %A lym q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)

        input_ = 'red~score %A lym q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Making ly ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Removing {illustrate.trim()} ...' in transcript
        assert f'Writing {illustrate.trim()} ...' in transcript
        assert f'Interpreting {illustrate.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert f'Opening {target.trim()} ...' not in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)
