% Red Example Score (2013) for piano 

\version "2.19.15"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "../../stylesheets/stylesheet.ily"

\score {
    {
    \include "../_segments/segment-01.ly"
    \include "../_segments/segment-02.ly"
    \include "../_segments/segment-03.ly"
    }
}