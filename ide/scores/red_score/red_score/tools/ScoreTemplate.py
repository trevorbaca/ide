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

            >>> from red_score import tools
            >>> template = tools.ScoreTemplate()
            >>> score = template()

            >>> f(score)
            \context Score = "RedScore"
            <<
                \context StaffGroup = "PianoStaffGroup"
                <<
                    \context RHStaff = "RHStaff"
                    {
                        \context RH_Voice = "RH_Voice"
                        {
                        }
                    }
                    \context LHStaff = "LHStaff"
                    {
                        \context LH_Voice = "LH_Voice"
                        {
                        }
                    }
                >>
            >>

        Returns score.
        """
        rh_voice = abjad.Voice(lilypond_type="RH_Voice", name="RH_Voice")
        rh_staff = abjad.Staff(
            [rh_voice], lilypond_type="RHStaff", name="RHStaff"
        )
        lh_voice = abjad.Voice(lilypond_type="LH_Voice", name="LH_Voice")
        lh_staff = abjad.Staff(
            [lh_voice], lilypond_type="LHStaff", name="LHStaff"
        )
        piano_staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff], name="PianoStaffGroup"
        )
        score = abjad.Score([piano_staff_group], name="RedScore")
        return score
