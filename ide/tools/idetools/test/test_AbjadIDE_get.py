import abjad
import ide
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_get_01():
    r'''In build directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').build('letter', 'front-cover.tex')
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu %letter get red~score ont-co y q')
        assert target.is_file()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : builds : letter (empty)'
        header += ' : get files from ...'
        assert header in transcript
        assert header in transcript
        header = 'Blue Score (2017) : distribution (empty)'
        header += ' : get Red Score (2017) files ...'
        assert f'> red score' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_02():
    r'''In distribution directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').distribution / 'red-score.pdf'
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu dd get red~score ore.pdf y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : distribution (empty)'
        header += ' : get files from ...'
        assert header in transcript
        header = 'Blue Score (2017) : distribution (empty)'
        header += ' : get Red Score (2017) files ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> ore.pdf' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_03():
    r'''In etc directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').etc / 'notes.txt'
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu ee get red~score otes.txt y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : etc (empty) : get files from ...'
        assert header in transcript
        header = 'Blue Score (2017) : etc (empty)'
        header += ' : get Red Score (2017) files ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> otes.txt' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_04():
    r'''In material directory.
    '''

    with ide.Test():
        source = ide.Path('blue_score')
        source = source.materials / 'dynamics' / 'definition.py'
        assert source.is_file()
        target = source.with_parent('staccati')
        target.remove()

        abjad_ide(f'blu mm staccati get dyn y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials : staccati (empty)'
        header += ' : get file ...'
        assert header in transcript
        for name in [
            'dynamics',
            'sargasso_measures', 
            'talea_rhythm_maker',
            ]:
            path = source.materials / name / 'definition.py'
            assert path.trim() in transcript
        assert f'> dyn' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_05():
    r'''In materials directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').materials / 'magic_numbers'
        assert source.is_dir()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu mm get red~score agic y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : materials : get packages from ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> agic' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_06():
    r'''In segment directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments.definition('segment_02')
        assert source.is_file()
        target = source.with_parent('segment_03')
        target.remove()

        abjad_ide(f'red %C get segment_02 y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Red Score (2017) : segments : C : get file ...'
        assert header in transcript
        assert f'> segment_02' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_07():
    r'''In segments directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').segments / 'segment_03'
        assert source.is_dir()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu gg get red~score C y <return> q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : segments : get packages from ...'
        assert header in transcript
        header = 'Blue Score (2017) : segments'
        header += ' : get Red Score (2017) packages ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> C' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript
        assert 'Name metadatum> ' in transcript


def test_AbjadIDE_get_08():
    r'''In stylesheets directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').stylesheets / 'stylesheet.ily'
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu yy get red~score eet.i y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : stylesheets (empty) : get files from ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> eet.i' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_09():
    r'''In test directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').test / 'test_materials.py'
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu tt get red~score _mat y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : test (empty) : get files from ...'
        assert header in transcript
        assert '> red score' in transcript
        assert '> _mat' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript


def test_AbjadIDE_get_10():
    r'''In tools directory.
    '''

    with ide.Test():
        source = ide.Path('red_score').tools / 'ScoreTemplate.py'
        assert source.is_file()
        target = source.with_score('blue_score')
        target.remove()

        abjad_ide(f'blu oo get red~score ST y q')
        assert target.exists()
        transcript = abjad_ide.io.transcript
        header = 'Blue Score (2017) : tools : get files from ...'
        assert header in transcript
        assert f'> red score' in transcript
        assert f'Getting {source.trim()} ...' in transcript
        assert f'Will write {target.trim()} ...' in transcript
        assert 'Ok?> y' in transcript
        assert f'Writing {target.trim()} ...' in transcript
