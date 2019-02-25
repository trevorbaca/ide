\version "2.19.82"                                                             %! LilyPondFile
\language "english"                                                            %! LilyPondFile

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/stylesheet.ily"                                    %! LilyPondFile

\header {                                                                      %! LilyPondFile
    tagline = ##f
}                                                                              %! LilyPondFile

\layout {}
\include "illustration.ily"                                                    %! extern
\paper {}


\score {                                                                       %! LilyPondFile
    <<
        {
            \include "layout.ly"
        }
        \context Score = "Two_Staff_Piano_Score"                               %! abjad.TwoStaffPianoScoreTemplate.__call__
        <<                                                                     %! abjad.TwoStaffPianoScoreTemplate.__call__
            \context GlobalContext = "Global_Context"                          %! abjad.ScoreTemplate._make_global_context
            <<                                                                 %! abjad.ScoreTemplate._make_global_context
                \context GlobalRests = "Global_Rests"                          %! abjad.ScoreTemplate._make_global_context
                {                                                              %! abjad.ScoreTemplate._make_global_context
                }                                                              %! abjad.ScoreTemplate._make_global_context
                \context GlobalSkips = "Global_Skips"                          %! abjad.ScoreTemplate._make_global_context
                {                                                              %! abjad.ScoreTemplate._make_global_context
                }                                                              %! abjad.ScoreTemplate._make_global_context
            >>                                                                 %! abjad.ScoreTemplate._make_global_context
            \context PianoStaff = "Piano_Staff"                                %! abjad.TwoStaffPianoScoreTemplate.__call__
            <<                                                                 %! abjad.TwoStaffPianoScoreTemplate.__call__
                \context Staff = "RH_Staff"                                    %! abjad.TwoStaffPianoScoreTemplate.__call__
                {                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
                    \context Voice = "RH_Voice"                                %! abjad.TwoStaffPianoScoreTemplate.__call__
                    {                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                        g''4.
                        bf''4.
                        d''4.
                        g'4.
                        cs'8.
                        af'8.
                        a'8.
                        e''8.
                        bf''4
                        ~
                        bf''16
                        c'4
                        ~
                        c'16
                        fs'4
                        ~
                        fs'16
                        bf'4
                        ~
                        bf'16
                        a''4
                        ~
                        a''16
                        bf''4
                        ~
                        bf''16
                    }                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                }                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
                \context Staff = "LH_Staff"                                    %! abjad.TwoStaffPianoScoreTemplate.__call__
                {                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
                    \context Voice = "LH_Voice"                                %! abjad.TwoStaffPianoScoreTemplate.__call__
                    {                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                        \clef "bass"                                           %! abjad.ScoreTemplate.attach_defaults
                        fs4
                        ~
                        fs16
                        d,4
                        ~
                        d,16
                        a4
                        ~
                        a16
                        g,4
                        ~
                        g,16
                        cs4
                        ~
                        cs16
                        a4
                        ~
                        a16
                        b,4.
                        bf,4.
                        c4.
                        e,4.
                        bf8.
                        af,8.
                        bf8.
                        fs8.
                    }                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                }                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
            >>                                                                 %! abjad.TwoStaffPianoScoreTemplate.__call__
        >>                                                                     %! abjad.TwoStaffPianoScoreTemplate.__call__
    >>
}                                                                              %! LilyPondFile