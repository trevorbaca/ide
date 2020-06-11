#(set-default-paper-size "letter" 'portrait)
#(set-global-staff-size 14)

\include "contexts.ily"

\paper {
    evenFooterMarkup = \markup {}
    evenHeaderMarkup = \markup {}
    left-margin = 14
    %markup-system-spacing.minimum-distance = 36
    oddFooterMarkup = \markup {}
    oddHeaderMarkup = \markup {}
    print-all-headers = ##t
    score-system-spacing.minimum-distance = 12
    top-markup-spacing.minimum-distance = 6
}

\layout {
    \accidentalStyle neo-modern
    indent = 5
    ragged-bottom = ##t
    ragged-last = ##t
    ragged-right = ##t
}

