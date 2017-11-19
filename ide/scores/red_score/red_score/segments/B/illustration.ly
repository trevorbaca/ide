\version "2.19.80"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/stylesheet.ily"

\header {}

\layout {}

\paper {}

\score {
    \context Score = "Two-Staff Piano Score" <<
        \context GlobalContext = "Global Context" {
            { % measure
                \time 6/8
                s1 * 3/4
            } % measure
            { % measure
                s1 * 3/4
            } % measure
        }
        \context PianoStaff = "Piano Staff" <<
            \context Staff = "RH Staff" {
                \context Voice = "RH Voice" {
                    \set PianoStaff.instrumentName = \markup { Piano }
                    \set PianoStaff.shortInstrumentName = \markup { Pf. }
                    \clef "treble"
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
            \context Staff = "LH Staff" {
                \context Voice = "LH Voice" {
                    \clef "bass"
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
}