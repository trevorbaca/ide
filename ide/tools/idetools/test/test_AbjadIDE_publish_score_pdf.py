import abjad
import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_publish_score_pdf_01():

    score_pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'distribution',
        'red-score-score.pdf',
        )

    assert score_pdf_path.exists()

    with ide.Test():
        score_pdf_path.unlink()
        input_ = 'red~score bb letter spp q'
        abjad_ide._start(input_=input_)
        assert score_pdf_path.exists()
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Copied' in contents
    assert 'FROM' in contents
    assert 'TO' in contents
