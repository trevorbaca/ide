import abjad


class ScoreTemplate(object):
    """
    Score template.
    """

    ### INITIALIZER ###

    def __init__(self):
        dictionary = abjad.OrderedDict()
        self.context_name_abbreviations = dictionary

    ### SPECIAL METHODS ###

    def __call__(self):
        r"""
        Calls score template.

        ..  container:: example

            >>> import red_score
            >>> red_score.ScoreTemplate()
            <red_score.ScoreTemplate.ScoreTemplate object at 0x...>

        Returns score.
        """
        rh_voice = abjad.Voice(lilypond_type="RH_Voice", name="RH_Voice")
        rh_staff = abjad.Staff([rh_voice], lilypond_type="RHStaff", name="RHStaff")
        lh_voice = abjad.Voice(lilypond_type="LH_Voice", name="LH_Voice")
        lh_staff = abjad.Staff([lh_voice], lilypond_type="LHStaff", name="LHStaff")
        piano_staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff], name="PianoStaffGroup"
        )
        score = abjad.Score([piano_staff_group], name="RedScore")
        return score
