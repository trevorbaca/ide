import abjad
import baca


instruments = abjad.OrderedDict([
    (
        'BassClarinet',
        abjad.BassClarinet(
            name='bass clarinet',
            markup=baca.markup.instrument('Bass clarinet'),
            short_name='b. cl.',
            short_markup=baca.markup.short_instrument('B. cl.'),
            ),
        ),
    (
        'Violin',
        abjad.Violin(
            context='StaffGroup',
            markup=baca.markup.instrument('Violin'),
            short_markup=baca.markup.short_instrument('Vn.'),
            )
        ),
    (
        'Viola',
        abjad.Viola(
            context='StaffGroup',
            markup=baca.markup.instrument('Viola'),
            short_markup=baca.markup.short_instrument('Va.'),
            ),
        ),
    (
        'Cello',
        abjad.Cello(
            context='StaffGroup',
            markup=baca.markup.instrument('Cello'),
            short_markup=baca.markup.short_instrument('Vc.'),
            ),
        ),
    ])
