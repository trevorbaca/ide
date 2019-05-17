import baca


breaks = baca.breaks(baca.page([1, 60, (15, 20)]))

spacing = baca.scorewide_spacing(
    __file__,
    breaks=breaks,
    fallback_duration=(1, 12),
    fermata_measure_duration=(1, 4),
)
