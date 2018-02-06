% measure_count = 12


\context Score = "Score"
<<
    \context GlobalContext = "GlobalContext"
    <<
        \context PageLayout = "PageLayout"
        {   %*% PageLayout
            
            % [PageLayout measure 1]                                                     %! SM4
            \autoPageBreaksOff                                                           %! BREAK:BMM1
            \noBreak                                                                     %! BREAK:BMM2
            \overrideProperty Score.NonMusicalPaperColumn.line-break-system-details      %! BREAK:IC
            #'((Y-offset . 20) (alignment-distances . (15 20)))                          %! BREAK:IC
            \pageBreak                                                                   %! BREAK:IC
            s1 * 9/2
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <0>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 2]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 9/2
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <1>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 3]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <2>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 4]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <3>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 5]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <4>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 6]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <5>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 7]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <6>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 8]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <7>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 9]                                                     %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <8>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 10]                                                    %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <9>                                                              %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 11]                                                    %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <10>                                                             %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
            % [PageLayout measure 12]                                                    %! SM4
            \noBreak                                                                     %! BREAK:BMM2
            s1 * 3/4
        %@% ^ \markup {                                                                  %! MEASURE_INDEX_MARKUP:SM32
        %@%     \fontsize                                                                %! MEASURE_INDEX_MARKUP:SM32
        %@%         #3                                                                   %! MEASURE_INDEX_MARKUP:SM32
        %@%         \with-color                                                          %! MEASURE_INDEX_MARKUP:SM32
        %@%             #(x11-color 'DarkCyan)                                           %! MEASURE_INDEX_MARKUP:SM32
        %@%             <11>                                                             %! MEASURE_INDEX_MARKUP:SM32
        %@%     }                                                                        %! MEASURE_INDEX_MARKUP:SM32
            
        }   %*% PageLayout
    >>
>>