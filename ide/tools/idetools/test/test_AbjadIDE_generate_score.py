import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_score_01():

    target = ide.PackagePath('red_score').builds / 'letter' / 'score.tex'
    with ide.Test(keep=[target]):
        target.remove()

        input_ = 'red~score %letter sg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating score ...' in transcript
        assert f'Removing {target.trim()} ...' not in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)

        input_ = 'red~score %letter sg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._transcript
        assert 'Generating score ...' in transcript
        assert f'Removing {target.trim()} ...' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)
