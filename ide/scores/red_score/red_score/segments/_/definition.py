import abjad
import red_score


time_signatures = [(15, 8), (18, 8)]
rh_divisions = []
rh_divisions.extend(4 * [(3, 8)])
rh_divisions.extend(4 * [(3, 16)])
rh_divisions.extend(6 * [(5, 16)])
lh_divisions = []
lh_divisions.extend(6 * [(5, 16)])
lh_divisions.extend(4 * [(3, 8)])
lh_divisions.extend(4 * [(3, 16)])
divisions = {"RH_Voice": rh_divisions, "LH_Voice": lh_divisions}

maker = red_score.PianoStaffSegmentMaker(
    divisions=divisions,
    include_layout_ly=True,
    time_signatures=time_signatures,
)
