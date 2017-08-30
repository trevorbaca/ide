% Red Score (2017) for piano

\version "2.19.65"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"

\score {
    {
    \include "../_segments/segment-01.ly"
    \include "../_segments/segment-02.ly"
    \include "../_segments/segment-03.ly"
    }
}