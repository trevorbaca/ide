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
        source = ide.Path('red_score').builds / 'letter' / 'score.pdf'
        target = ide.Path('red_score').distribution / 'red-score.pdf'
        target.remove()

        abjad_ide('red~score bb letter fci pi mi bci si spp q')
        transcript = abjad_ide.io_manager.transcript
        assert 'Publishing score PDF ...' in transcript
        assert f'FROM: {source.trim()}' in transcript
        assert f'  TO: {target.trim()}' in transcript
        assert target.exists()
