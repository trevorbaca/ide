import abjad
import definition
import pathlib


def make_lilypond_file():
    r'''Reimplement for material-specific illustration logic.
    '''
    name = pathlib.Path(__file__).parent.name
    title = name.replace('_', ' ').capitalize()
    title = abjad.Markup(title)
    title = title.override(('font-name', 'Palatino'))
    material = getattr(definition, name)
    try:
        lilypond_file = material.__illustrate__(title=title)
    except TypeError:
        lilypond_file = material.__illustrate__()
    return lilypond_file


lilypond_file = make_lilypond_file()
