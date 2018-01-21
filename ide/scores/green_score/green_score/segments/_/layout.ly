\context Score = "Score" <<
    \context GlobalContext = "GlobalContext" <<
        \context PageLayout = "PageLayout" {
            
            % PageLayout [measure 1]                                                     %! SM4
            \newSpacingSection                                                           %! SPACING:HSS1
            \set Score.proportionalNotationDuration = #(ly:make-moment 1 12)             %! SPACING:HSS1
            \autoPageBreaksOff                                                           %! BREAK:BMM1
            \noBreak                                                                     %! BREAK:BMM2
            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
            #'((Y-offset . 60) (alignment-distances . (15 20)))                          %! BREAK:IC
            \pageBreak                                                                   %! BREAK:IC
            s1 * 7/4
        %@% ^ \markup {                                                                  %! SPACING_MARKUP:HSS2
        %@%     \with-color                                                              %! SPACING_MARKUP:HSS2
        %@%         #(x11-color 'ForestGreen)                                            %! SPACING_MARKUP:HSS2
        %@%         \fontsize                                                            %! SPACING_MARKUP:HSS2
        %@%             #3                                                               %! SPACING_MARKUP:HSS2
        %@%             [1/12]                                                           %! SPACING_MARKUP:HSS2
        %@%     }                                                                        %! SPACING_MARKUP:HSS2
            
            % PageLayout [measure 2]                                                     %! SM4
            \newSpacingSection                                                           %! SPACING:HSS1
            \set Score.proportionalNotationDuration = #(ly:make-moment 35 96)            %! SPACING:HSS1
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 1/4
        %@% ^ \markup {                                                                  %! SPACING_MARKUP:HSS2
        %@%     \with-color                                                              %! SPACING_MARKUP:HSS2
        %@%         #(x11-color 'ForestGreen)                                            %! SPACING_MARKUP:HSS2
        %@%         \fontsize                                                            %! SPACING_MARKUP:HSS2
        %@%             #3                                                               %! SPACING_MARKUP:HSS2
        %@%             [[35/96]]                                                        %! SPACING_MARKUP:HSS2
        %@%     }                                                                        %! SPACING_MARKUP:HSS2
            
        }
    >>
>>