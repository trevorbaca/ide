import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_front_cover_source_02():

    cover_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )

    with abjad.FilesystemState(keep=[cover_path]):
        cover_path.unlink()
        assert not cover_path.exists()
        input_ = 'red~example~score bb letter-portrait fcg q'
        abjad_ide._start(input_=input_)
        assert cover_path.is_file()

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Writing' in contents
