\version "2.19.80"
\language "english"

\header {}

\layout {
    \accidentalStyle forget
    indent = #0
}

\paper {
    markup-system-spacing.padding = 8
    system-system-spacing.padding = 10
    top-markup-spacing.padding = 4
}

\score {
    \new Score \with {
        \override BarLine.transparent = ##t
        \override BarNumber.stencil = ##f
        \override Beam.stencil = ##f
        \override Flag.stencil = ##f
        \override Stem.stencil = ##f
        \override TimeSignature.stencil = ##f
        proportionalNotationDuration = #(ly:make-moment 1 12)
    } <<
        \new Staff {
            \new Voice {
                fs'8
                b'8
                g'8
                cs'8
                ef'8
                e'8
                \bar "|."
                \override Score.BarLine.transparent = ##f
            }
        }
    >>
}