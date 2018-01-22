import abjad
import ide
abjad_ide = ide.AbjadIDE(test=True)


def test_AbjadIDE_make_parts_directory_01():

    with ide.Test():
        directory = ide.Path('green_score', 'builds', 'arch-a-parts')
        assert not directory.exists()

        abjad_ide('gre bb parts arch-a-parts arch~a ARCH-A y q')
        transcript = abjad_ide.io.transcript
        lines = transcript.lines
        assert 'Getting part names from score template ...' in lines
        assert 'Found BassClarinet ...' in lines
        assert 'Found Violin ...' in lines
        assert 'Found Viola ...' in lines
        assert 'Found Cello ...' in lines

        assert 'Directory name> arch-a-parts' in lines
        assert 'Paper size> arch a' in lines
        assert 'Catalog number suffix> ARCH-A' in lines
        assert 'Will make ...' in lines
        for line in [
            '    green_score/builds/arch-a-parts',
            '    green_score/builds/arch-a-parts/stylesheet.ily',
            '    green_score/builds/arch-a-parts/bass-clarinet-front-cover.tex',
            '    green_score/builds/arch-a-parts/bass-clarinet-preface.tex',
            '    green_score/builds/arch-a-parts/bass-clarinet-music.ly',
            '    green_score/builds/arch-a-parts/bass-clarinet-back-cover.tex',
            '    green_score/builds/arch-a-parts/bass-clarinet-part.tex',
            '    green_score/builds/arch-a-parts/violin-front-cover.tex',
            '    green_score/builds/arch-a-parts/violin-preface.tex',
            '    green_score/builds/arch-a-parts/violin-music.ly',
            '    green_score/builds/arch-a-parts/violin-back-cover.tex',
            '    green_score/builds/arch-a-parts/violin-part.tex',
            '    green_score/builds/arch-a-parts/viola-front-cover.tex',
            '    green_score/builds/arch-a-parts/viola-preface.tex',
            '    green_score/builds/arch-a-parts/viola-music.ly',
            '    green_score/builds/arch-a-parts/viola-back-cover.tex',
            '    green_score/builds/arch-a-parts/viola-part.tex',
            '    green_score/builds/arch-a-parts/cello-front-cover.tex',
            '    green_score/builds/arch-a-parts/cello-preface.tex',
            '    green_score/builds/arch-a-parts/cello-music.ly',
            '    green_score/builds/arch-a-parts/cello-back-cover.tex',
            '    green_score/builds/arch-a-parts/cello-part.tex',
            ]:
            assert line in lines, repr(line)

        assert 'Ok?> y' in lines

        for line in [
            'Collecting segment lys ...',
            'Writing green_score/builds/arch-a-parts/_segments/segment-_.ly ...',
            'No + tags to deactivate in arch-a-parts ...',
            'No -ARCH_A_PARTS* tags to deactivate in arch-a-parts ...',
            'No +ARCH_A_PARTS* tags to activate in arch-a-parts ...',
            'No EOL_FERMATA tags to activate in arch-a-parts ...',
            'No SHIFTED_CLEF tags to activate in arch-a-parts ...',
            'Deactivating 26 persistent indicator color expression tags in arch-a-parts ...',
            'Activating 1 persistent indicator color suppression tag in arch-a-parts ...',
            'Deactivating 1 colored markup tag in arch-a-parts ...',
            'Generating stylesheet ...',
            'Writing green_score/builds/arch-a-parts/stylesheet.ily ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-back-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-front-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-music.ly ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-part.tex ...',
            'Writing green_score/builds/arch-a-parts/bass-clarinet-preface.tex ...',
            'Writing green_score/builds/arch-a-parts/bass_clarinet_layout.py ...',
            'Writing green_score/builds/arch-a-parts/violin-back-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/violin-front-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/violin-music.ly ...',
            'Writing green_score/builds/arch-a-parts/violin-part.tex ...',
            'Writing green_score/builds/arch-a-parts/violin-preface.tex ...',
            'Writing green_score/builds/arch-a-parts/violin_layout.py ...',
            'Writing green_score/builds/arch-a-parts/viola-back-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/viola-front-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/viola-music.ly ...',
            'Writing green_score/builds/arch-a-parts/viola-part.tex ...',
            'Writing green_score/builds/arch-a-parts/viola-preface.tex ...',
            'Writing green_score/builds/arch-a-parts/viola_layout.py ...',
            'Writing green_score/builds/arch-a-parts/cello-back-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/cello-front-cover.tex ...',
            'Writing green_score/builds/arch-a-parts/cello-music.ly ...',
            'Writing green_score/builds/arch-a-parts/cello-part.tex ...',
            'Writing green_score/builds/arch-a-parts/cello-preface.tex ...',
            'Writing green_score/builds/arch-a-parts/cello_layout.py ...',
            ]:
            assert line in lines, repr(line)

        assert directory.is_parts()
        assert directory('__metadata__.py').is_file()
        assert directory._assets.exists()
        assert directory._assets('.gitignore').is_file()
        assert directory._segments.exists()
        assert directory._segments('.gitignore').is_file()
        assert directory._segments('segment-_.ly').is_file()

        for name in [
            'bass-clarinet-back-cover.tex',
            'bass-clarinet-front-cover.tex',
            'bass-clarinet-music.ly',
            'bass-clarinet-part.tex',
            'bass-clarinet-preface.tex',
            'bass_clarinet_layout.py',
            'cello-back-cover.tex',
            'cello-front-cover.tex',
            'cello-music.ly',
            'cello-part.tex',
            'cello-preface.tex',
            'cello_layout.py',
            'stylesheet.ily',
            'viola-back-cover.tex',
            'viola-front-cover.tex',
            'viola-music.ly',
            'viola-part.tex',
            'viola-preface.tex',
            'viola_layout.py',
            'violin-back-cover.tex',
            'violin-front-cover.tex',
            'violin-music.ly',
            'violin-part.tex',
            'violin-preface.tex',
            'violin_layout.py',
            ]:
            path = directory(name)
            assert path.is_file(), repr(path)
