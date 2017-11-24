% Red Score (2017) for piano

\version "2.19.80"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"

\score {
    {
    \include "../_segments/segment-_.ly"
    \include "../_segments/segment-A.ly"
    \include "../_segments/segment-B.ly"
    }
}