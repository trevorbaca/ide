\context Score = "Score" \with {
    currentBarNumber = #3
} <<
    \context GlobalContext = "GlobalContext" <<
        \context PageLayout = "PageLayout" {
            
            % PageLayout [measure 3]                                                     %! SM4
            \autoPageBreaksOff                                                           %! BREAK:BMM1
            \noBreak                                                                     %! BREAK:BMM2
            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
            #'((Y-offset . 20) (alignment-distances . (15 20)))                          %! BREAK:IC
            \pageBreak                                                                   %! BREAK:IC
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <0>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % PageLayout [measure 4]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <1>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % PageLayout [measure 5]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <2>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % PageLayout [measure 6]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <3>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
        }
    >>
>>