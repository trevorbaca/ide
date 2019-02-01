import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_build_part_pdf_01():

    with ide.Test():
        parts = ide.Path('green_score', 'builds', 'arch-a-parts')
        assert not parts.exists()

        abjad_ide(
            'gre bb new parts arch-a-parts arch~a ARCH-A y'
            ' arch-a-parts ppb bass q'
            )
        lines = abjad_ide.io.transcript.lines
        index = lines.index('Select files to build> bass')
        lines = lines[index:]
        for line in [
            'Select files to build> bass',
            '',
            'Building green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet.pdf ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet/__make_layout_ly__.py ...',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/__make_layout_ly__.py ...',
            'Removing green_score/builds/arch-a-parts/bass-clarinet/__make_layout_ly__.py ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-front-cover.tex ...',
            'Found green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-front-cover.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-preface.tex ...',
            'Found green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-preface.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-music.ly ...',
            'ERROR IN LILYPOND LOG FILE ...',
            'Found green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-music.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-back-cover.tex ...',
            'Found green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-back-cover.pdf ...',
            '',
            'Interpreting green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-part.tex ...',
            'Found green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-part.pdf ...',
            '',
            'Opening green_score/builds/arch-a-parts/bass-clarinet/bass-clarinet-part.pdf ...',
            '',
            '> q',
            '',
            ]:
            assert line in lines
