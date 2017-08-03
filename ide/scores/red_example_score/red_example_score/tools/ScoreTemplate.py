import abjad


class ScoreTemplate(abjad.AbjadObject):
    r'''Score template.
    '''

    ### INITIALIZER ###

    def __init__(self):
        dictionary = abjad.TypedOrderedDict()
        self.context_name_abbreviations = dictionary

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        ..  container:: example

            >>> from red_example_score import tools
            >>> template = tools.ScoreTemplate()
            >>> score = template()

        ::

            >>> f(score)
            \context Score = "Red Example Score" <<
                \context StaffGroup = "Piano Staff Group" <<
                    \context RHStaff = "RH Staff" {
                        \context RHVoice = "RH Voice" {
                        }
                    }
                    \context LHStaff = "LH Staff" {
                        \context LHVoice = "LH Voice" {
                        }
                    }
                >>
            >>

        Returns score.
        '''
        rh_voice = abjad.Voice(
            context_name='RHVoice',
            name='RH Voice',
            )
        rh_staff = abjad.Staff(
            [rh_voice],
            context_name='RHStaff',
            name='RH Staff',
            )
        lh_voice = abjad.Voice(
            context_name='LHVoice',
            name='LH Voice',
            )
        lh_staff = abjad.Staff(
            [lh_voice],
            context_name='LHStaff',
            name='LH Staff',
            )
        piano_staff_group = abjad.StaffGroup(
            [
                rh_staff,
                lh_staff,
                ],
            name='Piano Staff Group',
            )
        score = abjad.Score(
            [
                piano_staff_group,
            ],
            name='Red Example Score',
            )
        return score
