import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(is_test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_publish_score_pdf_01():

    with ide.Test():
        source = ide.Path('red_score').build / 'letter' / 'score.pdf'
        target = ide.Path('red_score').distribution / 'red-score.pdf'
        target.remove()

        input_ = 'red~score bb letter fci pi mi bci si spp q'
        abjad_ide._start(input_=input_)
        transcript = abjad_ide._io_manager._transcript.contents
        assert 'Publishing score PDF ...' in transcript
        assert f'FROM: {abjad_ide._trim(source)}' in transcript
        assert f'  TO: {abjad_ide._trim(target)}' in transcript
        assert target.exists()
