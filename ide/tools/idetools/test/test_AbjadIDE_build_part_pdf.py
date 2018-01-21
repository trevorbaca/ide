import ide
import os
import pytest
abjad_ide = ide.AbjadIDE(test=True)


#@pytest.mark.skipif(
#    os.environ.get('TRAVIS') == 'true',
#    reason="Travis-CI can not find fonts for XeTeX tests."
#    )
#def test_AbjadIDE_build_part_pdf_01():
#
#    with ide.Test():
#        abjad_ide(
#            'gre bb parts arch-a-parts arch~a ARCH-A y'
#            ' arch-a-parts apb bass-clarinet q'
#            )
#        lines = abjad_ide.io.transcript.lines
#        line = 'Match name> bass-clarinet'
#        index = lines.index(line)
#        assert lines[index:] == [
#            ]
