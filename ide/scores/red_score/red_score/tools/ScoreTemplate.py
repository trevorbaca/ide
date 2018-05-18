import abjad


class ScoreTemplate(abjad.AbjadObject):
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
                        \context RHVoice = "RHVoice"
                        {
                        }
                    }
                    \context LHStaff = "LHStaff"
                    {
                        \context LHVoice = "LHVoice"
                        {
                        }
                    }
                >>
            >>

        Returns score.
        """
        rh_voice = abjad.Voice(
            lilypond_type='RHVoice',
            name='RHVoice',
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            lilypond_type='RHStaff',
            name='RHStaff',
            )
        lh_voice = abjad.Voice(
            lilypond_type='LHVoice',
            name='LHVoice',
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            lilypond_type='LHStaff',
            name='LHStaff',
            )
        piano_staff_group = abjad.StaffGroup(
            [rh_staff, lh_staff],
            name='PianoStaffGroup',
            )
        score = abjad.Score(
            [piano_staff_group],
            name='RedScore',
            )
        return score
