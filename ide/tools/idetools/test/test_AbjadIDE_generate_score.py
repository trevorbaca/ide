import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_generate_score_01():

    target = ide.Path('red_score').build / 'letter' / 'score.tex'
    with ide.Test(keep=[target]):
        target.remove()

        input_ = 'red~score %letter sg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating score ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' not in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)

        input_ = 'red~score %letter sg q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Generating score ...' in transcript
        assert f'Removing {abjad_ide._trim(target)} ...' in transcript
        assert f'Writing {abjad_ide._trim(target)} ...' in transcript
        assert target.is_file()
        assert abjad.TestManager._compare_backup(target)
