\version "2.19.65"
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
            \context Staff = "Treble Staff" {
                \clef "treble"
                s1 * 1/4
                s1 * 1/4
                c'1 * 1/4 \glissando
                c'''''1 * 1/4
            }
            \context Staff = "Bass Staff" {
                \clef "bass"
                a,,,1 * 1/4 \glissando
                \change Staff = "Treble Staff"
                c'1 * 1/4
                s1 * 1/4
                s1 * 1/4
            }
        >>
    >>
}