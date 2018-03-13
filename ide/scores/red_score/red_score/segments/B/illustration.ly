\version "2.19.80"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/stylesheet.ily"

\header {}

\layout {}

\paper {}
\include "illustration.ily"


\score {
    <<
        {
            \include "layout.ly"
        }
        \context Score = "TwoStaffPianoScore"
        <<
            \context GlobalContext = "GlobalContext"
            <<
                \context GlobalRests = "GlobalRests"
                {
                }
                \context GlobalSkips = "GlobalSkips"
                {
                }
            >>
            \context PianoStaff = "PianoStaff"
            <<
                \context Staff = "RHStaff"
                {
                    \context Voice = "RHVoice"
                    {
                        g''8
                        bf''8
                        d''8
                        g'8
                        cs'8
                        af'8
                        a'4.
                        e''4.
                        bf''4.
                        c'8
                        fs'8
                        bf'8
                        a''8
                        bf''8
                        f''8
                        e'4.
                        b''4.
                        bf'4.
                    }
                }
                \context Staff = "LHStaff"
                {
                    \context Voice = "LHVoice"
                    {
                        \set PianoStaff.instrumentName = \markup { Piano }               %! ST1
                        \set PianoStaff.shortInstrumentName = \markup { Pf. }            %! ST1
                        \clef "bass"                                                     %! ST3
                        fs4.
                        d,4.
                        a4.
                        g,8
                        cs8
                        a8
                        b,8
                        bf,8
                        c8
                        e,4.
                        bf4.
                        af,4.
                        bf8
                        fs8
                        f,8
                        bf8
                        af,8
                        bf8
                    }
                }
            >>
        >>
    >>
}