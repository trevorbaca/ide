import abjad
from red_score.materials.red_pitch_classes.definition import red_pitch_classes


numerators = [_.number for _ in red_pitch_classes]
numerators = [_ % 11 + 1 for _ in numerators]
pairs = [(_, 8) for _ in numerators]
time_signatures = [abjad.TimeSignature(_) for _ in pairs]
