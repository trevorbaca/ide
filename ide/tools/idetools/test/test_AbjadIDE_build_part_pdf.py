import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Travis-CI can not find fonts for XeTeX tests."
    )
def test_AbjadIDE_build_part_pdf_01():

    with ide.Test():
        parts = ide.Path('green_score', 'builds', 'arch-a-parts')
        assert not parts.exists()

        abjad_ide(
            'gre bb parts arch-a-parts arch~a ARCH-A y'
            ' arch-a-parts apb bass q'
            )
        lines = abjad_ide.io.transcript.lines
        index = lines.index('Match name> bass')
        assert lines[index:] == [
            'Match name> bass',
            '',
            'Writing green_score/builds/arch-a-parts/__make_layout_ly__.py ...',
            'Interpreting green_score/builds/arch-a-parts/__make_layout_ly__.py ...',
            'Removing green_score/builds/arch-a-parts/__make_layout_ly__.py ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet-front-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-front-cover.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet-preface.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-preface.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet-music.ly ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-music.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet-back-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-back-cover.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet-part.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-part.pdf ...',
            'Opening green_score/builds/arch-a-parts/bass-clarinet-part.pdf ...',
            '',
            '> q',
            '',
            ]
