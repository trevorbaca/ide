% 2017-01-07 10:07

\version "2.19.54"
\language "english"

\header {
    tagline = ##f
}

\score {
    \new Score \with {
        \override BarLine.stencil = ##f
        \override Glissando.thickness = #2
        \override SpanBar.stencil = ##f
        \override TimeSignature.stencil = ##f
    } <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                s1 * 1/4
                s1 * 1/4
                c'1 * 1/4 \glissando
                c'''''1 * 1/4
            }
            \context Staff = "bass" {
                \clef "bass"
                a,,,1 * 1/4 \glissando
                \change Staff = treble
                c'1 * 1/4
                s1 * 1/4
                s1 * 1/4
            }
        >>
    >>
}