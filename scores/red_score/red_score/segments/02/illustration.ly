\version "2.19.82"                                                             %! LilyPondFile
\language "english"                                                            %! LilyPondFile

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/stylesheet.ily"                                    %! LilyPondFile

\paper { first-page-number = #1 }                                              %! __make_segment_pdf__

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
                        g''4
                        bf''4
                        d''4
                        g'4
                        cs'8
                        af'8
                        a'8
                        e''8
                        bf''4.
                        c'4.
                        fs'4.
                        bf'4.
                        a''8.
                        bf''8.
                        f''8.
                        e'8.
                    }                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                }                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
                \context Staff = "LH_Staff"                                    %! abjad.TwoStaffPianoScoreTemplate.__call__
                {                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
                    \context Voice = "LH_Voice"                                %! abjad.TwoStaffPianoScoreTemplate.__call__
                    {                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                        \clef "bass"                                           %! abjad.ScoreTemplate.attach_defaults
                        fs4.
                        d,4.
                        a4.
                        g,4.
                        cs8.
                        a8.
                        b,8.
                        bf,8.
                        c4
                        e,4
                        bf4
                        af,4
                        bf8
                        fs8
                        f,8
                        bf8
                    }                                                          %! abjad.TwoStaffPianoScoreTemplate.__call__
                }                                                              %! abjad.TwoStaffPianoScoreTemplate.__call__
            >>                                                                 %! abjad.TwoStaffPianoScoreTemplate.__call__
        >>                                                                     %! abjad.TwoStaffPianoScoreTemplate.__call__
    >>
}                                                                              %! LilyPondFile