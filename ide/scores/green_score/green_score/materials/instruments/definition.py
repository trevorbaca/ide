import abjad
import baca


instruments = abjad.OrderedDict(
    [
        (
            "BassClarinet",
            abjad.BassClarinet(
                name="bass clarinet",
                markup=baca.markups.instrument("Bass clarinet"),
                short_name="b. cl.",
                short_markup=baca.markups.short_instrument("B. cl."),
            ),
        ),
        (
            "Violin",
            abjad.Violin(
                context="StaffGroup",
                markup=baca.markups.instrument("Violin"),
                short_markup=baca.markups.short_instrument("Vn."),
            ),
        ),
        (
            "Viola",
            abjad.Viola(
                context="StaffGroup",
                markup=baca.markups.instrument("Viola"),
                short_markup=baca.markups.short_instrument("Va."),
            ),
        ),
        (
            "Cello",
            abjad.Cello(
                context="StaffGroup",
                markup=baca.markups.instrument("Cello"),
                short_markup=baca.markups.short_instrument("Vc."),
            ),
        ),
    ]
)
