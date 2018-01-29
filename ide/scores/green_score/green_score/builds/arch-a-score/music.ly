% Green Score (2018) 

\version "2.19.81"
\language "english"

#(ly:set-option 'relative-includes #t)
\include "stylesheet.ily"


\score {
    <<
        {
        \include "layout.ly"
        }
        {
        \include "_segments/segment-_.ly"
        }
    >>
}
