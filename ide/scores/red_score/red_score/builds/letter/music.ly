% Red Score (2017) for piano

\version "2.19.65"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"

\score {
    {
    \include "../_segments/A.ly"
    \include "../_segments/B.ly"
    \include "../_segments/C.ly"
    }
}