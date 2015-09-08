# -*- encoding: utf-8 -*-
from abjad import *


class ScoreTemplate(abctools.AbjadObject):
    r'''Score template.
    '''

    ### INITIALIZER ###

    def __init__(self):
        dictionary = datastructuretools.TypedOrderedDict()
        self.context_name_abbreviations = dictionary

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        Returns LilyPondFile object.
        '''

        # make rh voice and staff
        rh_voice = Voice(
            context_name='RHVoice',
            name='RH Voice',
            )
        rh_staff = Staff(
            context_name='RHStaff',
            name='RH Staff',
            )

        # make lh voice and staff
        lh_voice = Voice(
            context_name='LHVoice',
            name='LH Voice',
            )
        lh_staff = Staff(
            context_name='LHStaff',
            name='LH Staff',
            )

        # maker piano staff group
        piano_staff_group = scoretools.StaffGroup(
            [
                rh_staff,
                lh_staff,
                ],
            name='Piano Staff Group',
            )

        # make score
        score = Score(
            [
                piano_staff_group,
            ],
            name='Red Example Score',
            )

        # return score
        return score