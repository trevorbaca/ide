import abjad
import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_generate_back_cover_source_01():

    source_path = pathlib.Path(
        configuration.abjad_ide_directory,
        'boilerplate',
        'back-cover.tex',
        )
    destination_path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'blue_example_score',
        'blue_example_score',
        'build',
        'letter-portrait',
        'back-cover.tex',
        )

    with source_path.open() as file_pointer:
        source_contents = ''.join(file_pointer.readlines())
    assert 'paper_size' in source_contents
    assert '{8.5in, 11in}' not in source_contents

    with abjad.FilesystemState(
        keep=[source_path], remove=[destination_path]):
        input_ = 'blue~example~score bb letter-portrait bcg q'
        abjad_ide._start(input_=input_)
        assert destination_path.is_file()
        with destination_path.open() as file_pointer:
            destination_contents = ''.join(file_pointer.readlines())
        assert 'paper_size' not in destination_contents
        assert '{8.5in, 11in}' in destination_contents

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Writing' in contents
