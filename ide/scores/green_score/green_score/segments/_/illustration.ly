\version "2.19.80"
\language "english"

#(ly:set-option 'relative-includes #t)

\include "../../stylesheets/stylesheet.ily"

\score {
    <<
        {
            \include "layout.ly"
        }
        \context Score = "Score" <<
            \tag BassClarinet.Violin.Viola.Cello                                         %! ST4
            \context GlobalContext = "GlobalContext" <<
                \context GlobalRests = "GlobalRests" {
                    
                    % GlobalRests [measure 1]                                            %! SM4
                    R1 * 7/4
                    
                    % GlobalRests [measure 2]                                            %! SM4
                    \once \override Score.MultiMeasureRest.transparent = ##t             %! SM19
                    \once \override Score.TimeSignature.stencil = ##f                    %! SM19
                    R1 * 1/4
                    ^ \markup {                                                          %! FIGURE_NAME_MARKUP:SM18
                        \musicglyph                                                      %! FIGURE_NAME_MARKUP:SM18
                            #"scripts.ulongfermata"                                      %! FIGURE_NAME_MARKUP:SM18
                        }                                                                %! FIGURE_NAME_MARKUP:SM18
                    
                }
                \context GlobalSkips = "GlobalSkips" {
                    
                    % GlobalSkips [measure 1]                                            %! SM4
                %@% \once \override TextSpanner.bound-details.left.text =                %! EXPLICIT_METRONOME_MARK:SM27
                %@% \markup {                                                            %! EXPLICIT_METRONOME_MARK:SM27
                %@%     \fontsize                                                        %! EXPLICIT_METRONOME_MARK:SM27
                %@%         #-6                                                          %! EXPLICIT_METRONOME_MARK:SM27
                %@%         \general-align                                               %! EXPLICIT_METRONOME_MARK:SM27
                %@%             #Y                                                       %! EXPLICIT_METRONOME_MARK:SM27
                %@%             #DOWN                                                    %! EXPLICIT_METRONOME_MARK:SM27
                %@%             \note-by-number                                          %! EXPLICIT_METRONOME_MARK:SM27
                %@%                 #2                                                   %! EXPLICIT_METRONOME_MARK:SM27
                %@%                 #0                                                   %! EXPLICIT_METRONOME_MARK:SM27
                %@%                 #1.5                                                 %! EXPLICIT_METRONOME_MARK:SM27
                %@%     \upright                                                         %! EXPLICIT_METRONOME_MARK:SM27
                %@%         {                                                            %! EXPLICIT_METRONOME_MARK:SM27
                %@%             =                                                        %! EXPLICIT_METRONOME_MARK:SM27
                %@%             58                                                       %! EXPLICIT_METRONOME_MARK:SM27
                %@%         }                                                            %! EXPLICIT_METRONOME_MARK:SM27
                %@%     \hspace                                                          %! EXPLICIT_METRONOME_MARK:SM27
                %@%         #1                                                           %! EXPLICIT_METRONOME_MARK:SM27
                %@%     }                                                                %! EXPLICIT_METRONOME_MARK:SM27 %! SM29
                    \once \override TextSpanner.Y-extent = ##f                           %! SM29
                    \once \override TextSpanner.bound-details.left-broken.text = ##f     %! SM29
                    \once \override TextSpanner.bound-details.left-broken.text = \markup {
                        \null
                        }                                                                %! SM29
                    \once \override TextSpanner.bound-details.left.stencil-align-dir-y = #center %! SM29
                    \once \override TextSpanner.bound-details.left.text =                %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                    \markup {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                        \with-color                                                      %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            #(x11-color 'blue)                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            {                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \fontsize                                                %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    #-6                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    \general-align                                       %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #Y                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        #DOWN                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        \note-by-number                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #2                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #0                                           %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                            #1.5                                         %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \upright                                                 %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    {                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        =                                                %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                        58                                               %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    }                                                    %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                \hspace                                                  %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                                    #1                                                   %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                            }                                                            %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15
                        }                                                                %! EXPLICIT_METRONOME_MARK_WITH_COLOR:SM15 %! SM29
                    \once \override TextSpanner.bound-details.right-broken.padding = 0   %! SM29
                    \once \override TextSpanner.bound-details.right-broken.text = ##f    %! SM29
                    \once \override TextSpanner.bound-details.right.padding = 0          %! SM29
                    \once \override TextSpanner.bound-details.right.stencil-align-dir-y = #center %! SM29
                    \once \override TextSpanner.dash-period = 0                          %! SM29
                    \time 7/4                                                            %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)       %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 7/4
                    \startTextSpan                                                       %! SM29
                    ^ \markup {
                        \column
                            {
                            %@% \line                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@%     {                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@%         \fontsize                                        %! MEASURE_NUMBER_MARKUP:SM31
                            %@%             #3                                           %! MEASURE_NUMBER_MARKUP:SM31
                            %@%             \with-color                                  %! MEASURE_NUMBER_MARKUP:SM31
                            %@%                 #(x11-color 'DarkCyan)                   %! MEASURE_NUMBER_MARKUP:SM31
                            %@%                 "[00 (1)]"                               %! MEASURE_NUMBER_MARKUP:SM31
                            %@%     }                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@% \line                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@%     {                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@%         \fontsize                                        %! STAGE_NUMBER_MARKUP:SM3
                            %@%             #3                                           %! STAGE_NUMBER_MARKUP:SM3
                            %@%             \with-color                                  %! STAGE_NUMBER_MARKUP:SM3
                            %@%                 #(x11-color 'DarkCyan)                   %! STAGE_NUMBER_MARKUP:SM3
                            %@%                 [1]                                      %! STAGE_NUMBER_MARKUP:SM3
                            %@%     }                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@% \line                                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%     {                                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%         \with-color                                      %! CLOCK_TIME_MARKUP:SM28
                            %@%             #(x11-color 'DarkCyan)                       %! CLOCK_TIME_MARKUP:SM28
                            %@%             \fontsize                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%                 #3                                       %! CLOCK_TIME_MARKUP:SM28
                            %@%                 [0'00'']                                 %! CLOCK_TIME_MARKUP:SM28
                            %@%     }                                                    %! CLOCK_TIME_MARKUP:SM28
                            }
                        }
                    
                    % GlobalSkips [measure 2]                                            %! SM4
                    \time 1/4                                                            %! EXPLICIT_TIME_SIGNATURE:SM8
                    \once \override Score.TimeSignature.color = #(x11-color 'blue)       %! EXPLICIT_TIME_SIGNATURE_COLOR:SM6
                    s1 * 1/4
                    \stopTextSpan                                                        %! SM29
                    ^ \markup {
                        \column
                            {
                            %@% \line                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@%     {                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@%         \fontsize                                        %! MEASURE_NUMBER_MARKUP:SM31
                            %@%             #3                                           %! MEASURE_NUMBER_MARKUP:SM31
                            %@%             \with-color                                  %! MEASURE_NUMBER_MARKUP:SM31
                            %@%                 #(x11-color 'DarkCyan)                   %! MEASURE_NUMBER_MARKUP:SM31
                            %@%                 "[01 (2)]"                               %! MEASURE_NUMBER_MARKUP:SM31
                            %@%     }                                                    %! MEASURE_NUMBER_MARKUP:SM31
                            %@% \line                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@%     {                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@%         \fontsize                                        %! STAGE_NUMBER_MARKUP:SM3
                            %@%             #3                                           %! STAGE_NUMBER_MARKUP:SM3
                            %@%             \with-color                                  %! STAGE_NUMBER_MARKUP:SM3
                            %@%                 #(x11-color 'DarkCyan)                   %! STAGE_NUMBER_MARKUP:SM3
                            %@%                 [2]                                      %! STAGE_NUMBER_MARKUP:SM3
                            %@%     }                                                    %! STAGE_NUMBER_MARKUP:SM3
                            %@% \line                                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%     {                                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%         \with-color                                      %! CLOCK_TIME_MARKUP:SM28
                            %@%             #(x11-color 'DarkCyan)                       %! CLOCK_TIME_MARKUP:SM28
                            %@%             \fontsize                                    %! CLOCK_TIME_MARKUP:SM28
                            %@%                 #3                                       %! CLOCK_TIME_MARKUP:SM28
                            %@%                 [0'07'']                                 %! CLOCK_TIME_MARKUP:SM28
                            %@%     }                                                    %! CLOCK_TIME_MARKUP:SM28
                            }
                        }
                    \override Score.BarLine.transparent = ##f                            %! SM5
                    \bar "|"                                                             %! SM5
                    
                }
            >>
            \context MusicContext = "MusicContext" {
                \context EnsembleStaffGroup = "EnsembleStaffGroup" <<
                    \tag BassClarinet                                                    %! ST4
                    \context BassClarinetMusicStaff = "BassClarinetMusicStaff" {
                        \context BassClarinetMusicVoice = "BassClarinetMusicVoice" {
                            
                            % BassClarinetMusicVoice [measure 1]                         %! SM4
                            \set BassClarinetMusicStaff.instrumentName = \markup {       %! DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                              %! DEFAULT_INSTRUMENT:SM8
                                    #16                                                  %! DEFAULT_INSTRUMENT:SM8
                                    \center-column                                       %! DEFAULT_INSTRUMENT:SM8
                                        {                                                %! DEFAULT_INSTRUMENT:SM8
                                            Bass                                         %! DEFAULT_INSTRUMENT:SM8
                                            clarinet                                     %! DEFAULT_INSTRUMENT:SM8
                                        }                                                %! DEFAULT_INSTRUMENT:SM8
                                }                                                        %! DEFAULT_INSTRUMENT:SM8
                            \set BassClarinetMusicStaff.shortInstrumentName = \markup {  %! DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                              %! DEFAULT_INSTRUMENT:SM8
                                    #10                                                  %! DEFAULT_INSTRUMENT:SM8
                                    \line                                                %! DEFAULT_INSTRUMENT:SM8
                                        {                                                %! DEFAULT_INSTRUMENT:SM8
                                            B.                                           %! DEFAULT_INSTRUMENT:SM8
                                            cl.                                          %! DEFAULT_INSTRUMENT:SM8
                                        }                                                %! DEFAULT_INSTRUMENT:SM8
                                }                                                        %! DEFAULT_INSTRUMENT:SM8
                            \set BassClarinetMusicStaff.forceClef = ##t                  %! DEFAULT_CLEF:SM8
                            \clef "treble"                                               %! DEFAULT_CLEF:SM8
                            \once \override BassClarinetMusicStaff.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                            \once \override BassClarinetMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                        %@% \override BassClarinetMusicStaff.Clef.color = ##f            %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                            R1 * 7/4
                            ^ \markup {
                                \column
                                    {
                                    %@% \line                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%     {                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             (“BassClarinet”                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \vcenter                                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             \hcenter-in                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 #16                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 \center-column                   %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     {                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         Bass                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         clarinet                 %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     }                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%         \concat                                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             {                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 \vcenter                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     \hcenter-in                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         #10                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                         \line                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                             {                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                                 B.               %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                                 cl.              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                             }                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                 \vcenter                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%                     )                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%             }                                    %! DEFAULT_INSTRUMENT_ALERT:SM10
                                    %@%     }                                            %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        \line                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            {                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                \with-color                              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    #(x11-color 'DarkViolet)             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    {                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            (“BassClarinet”              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \vcenter                         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \hcenter-in                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                #16                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \center-column           %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    {                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        Bass             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        clarinet         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    }                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        \concat                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            {                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \hcenter-in          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        #10              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \line            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            {            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                                B.       %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                                cl.      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            }            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \vcenter                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    )                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            }                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    }                                    %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            }                                            %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                    }
                                }
                            \set BassClarinetMusicStaff.instrumentName = \markup {       %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    #16                                                  %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \center-column                                       %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        {                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            Bass                                         %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            clarinet                                     %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                }                                                        %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                            \set BassClarinetMusicStaff.shortInstrumentName = \markup {  %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \hcenter-in                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    #10                                                  %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \line                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        {                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            B.                                           %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                            cl.                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        }                                                %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                }                                                        %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                            \override BassClarinetMusicStaff.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                            \override BassClarinetMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                            
                            % BassClarinetMusicVoice [measure 2]                         %! SM4
                            \stopStaff                                                   %! SM20
                            \once \override BassClarinetMusicStaff.StaffSymbol.line-count = 0 %! SM20
                            \startStaff                                                  %! SM20
                            \once \override BassClarinetMusicStaff.BarLine.bar-extent = #'(-2 . 2) %! SM20
                            R1 * 1/4
                            \once \override Score.BarLine.transparent = ##t              %! BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA:MEASURE_2:SM22
                            \once \override Score.SpanBar.transparent = ##t              %! BAR_LINE_ADJUSTMENT_AFTER_EOL_FERMATA:MEASURE_2:SM22
                            
                        }
                    }
                    \tag Violin                                                          %! ST4
                    \context ViolinStaffGroup = "ViolinStaffGroup" <<
                        \context ViolinRHMusicStaff = "ViolinRHMusicStaff" {
                            \context ViolinRHMusicVoice = "ViolinRHMusicVoice" {
                                
                                % ViolinRHMusicVoice [measure 1]                         %! SM4
                                \stopStaff                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override ViolinRHMusicStaff.StaffSymbol.line-count = 1 %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                              %! EXPLICIT_STAFF_LINES:SM8
                                \set ViolinRHMusicStaff.forceClef = ##t                  %! DEFAULT_CLEF:SM8
                                \clef "percussion"                                       %! DEFAULT_CLEF:SM8
                                \once \override ViolinRHMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolinRHMusicStaff.Clef.color = ##f            %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                \once \override ViolinRHMusicStaff.StaffSymbol.color = #(x11-color 'blue) %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                R1 * 7/4
                                \override ViolinRHMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                                
                                % ViolinRHMusicVoice [measure 2]                         %! SM4
                                \stopStaff                                               %! SM20
                                \once \override ViolinRHMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                R1 * 1/4
                                
                            }
                        }
                        \context ViolinMusicStaff = "ViolinMusicStaff" {
                            \context ViolinMusicVoice = "ViolinMusicVoice" {
                                
                                % ViolinMusicVoice [measure 1]                           %! SM4
                                \stopStaff                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override ViolinMusicStaff.StaffSymbol.line-count = 1 %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                              %! EXPLICIT_STAFF_LINES:SM8
                                \once \override TextScript.padding = #2.5                %! OC
                                \once \override TextScript.parent-alignment-X = #0       %! OC
                                \set ViolinStaffGroup.instrumentName = \markup {         %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! DEFAULT_INSTRUMENT:SM8
                                        Violin                                           %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set ViolinStaffGroup.shortInstrumentName = \markup {    %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! DEFAULT_INSTRUMENT:SM8
                                        Vn.                                              %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set ViolinMusicStaff.forceClef = ##t                    %! EXPLICIT_CLEF:SM8
                                \clef "percussion"                                       %! EXPLICIT_CLEF:SM8
                                \once \override ViolinStaffGroup.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolinMusicStaff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:SM6
                            %@% \override ViolinMusicStaff.Clef.color = ##f              %! EXPLICIT_CLEF_COLOR_CANCELLATION:SM7
                                \once \override ViolinMusicVoice.DynamicText.color = #(x11-color 'blue) %! EXPLICIT_DYNAMIC_COLOR:SM6
                                \once \override ViolinMusicStaff.StaffSymbol.color = #(x11-color 'blue) %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                c'1..
                                \effort_mf                                               %! EXPLICIT_DYNAMIC:SM8
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (“Violin”                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #16                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Violin                       %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Vn.                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (“Violin”                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #16                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Violin               %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Vn.          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            \line                                        %! IC
                                                {                                        %! IC
                                                    \whiteout                            %! IC
                                                        \upright                         %! IC
                                                            \override                    %! IC
                                                                #'(box-padding . 0.5)    %! IC
                                                                \box                     %! IC
                                                                    "grainfall (1)"      %! IC
                                                }                                        %! IC
                                        }
                                    }
                                \set ViolinStaffGroup.instrumentName = \markup {         %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Violin                                           %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolinStaffGroup.shortInstrumentName = \markup {    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vn.                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolinStaffGroup.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolinMusicStaff.Clef.color = #(x11-color 'DeepSkyBlue2) %! EXPLICIT_CLEF_REDRAW_COLOR:SM6
                                
                                % ViolinMusicVoice [measure 2]                           %! SM4
                                \stopStaff                                               %! SM20
                                \once \override ViolinMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                R1 * 1/4
                                
                            }
                        }
                    >>
                    \tag Viola                                                           %! ST4
                    \context ViolaStaffGroup = "ViolaStaffGroup" <<
                        \context ViolaRHMusicStaff = "ViolaRHMusicStaff" {
                            \context ViolaRHMusicVoice = "ViolaRHMusicVoice" {
                                
                                % ViolaRHMusicVoice [measure 1]                          %! SM4
                                \stopStaff                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override ViolaRHMusicStaff.StaffSymbol.line-count = 1 %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                              %! EXPLICIT_STAFF_LINES:SM8
                                \set ViolaRHMusicStaff.forceClef = ##t                   %! DEFAULT_CLEF:SM8
                                \clef "percussion"                                       %! DEFAULT_CLEF:SM8
                                \once \override ViolaRHMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolaRHMusicStaff.Clef.color = ##f             %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                \once \override ViolaRHMusicStaff.StaffSymbol.color = #(x11-color 'blue) %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                R1 * 7/4
                                \override ViolaRHMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                                
                                % ViolaRHMusicVoice [measure 2]                          %! SM4
                                \stopStaff                                               %! SM20
                                \once \override ViolaRHMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                R1 * 1/4
                                
                            }
                        }
                        \context ViolaMusicStaff = "ViolaMusicStaff" {
                            \context ViolaMusicVoice = "ViolaMusicVoice" {
                                
                                % ViolaMusicVoice [measure 1]                            %! SM4
                                \set ViolaStaffGroup.instrumentName = \markup {          %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! DEFAULT_INSTRUMENT:SM8
                                        Viola                                            %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set ViolaStaffGroup.shortInstrumentName = \markup {     %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! DEFAULT_INSTRUMENT:SM8
                                        Va.                                              %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set ViolaMusicStaff.forceClef = ##t                     %! DEFAULT_CLEF:SM8
                                \clef "alto"                                             %! DEFAULT_CLEF:SM8
                                \once \override ViolaStaffGroup.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override ViolaMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override ViolaMusicStaff.Clef.color = ##f               %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                R1 * 7/4
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (“Viola”                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #16                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Viola                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Va.                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (“Viola”                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #16                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Viola                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Va.          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                        }
                                    }
                                \set ViolaStaffGroup.instrumentName = \markup {          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Viola                                            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set ViolaStaffGroup.shortInstrumentName = \markup {     %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Va.                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override ViolaStaffGroup.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override ViolaMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                                
                                % ViolaMusicVoice [measure 2]                            %! SM4
                                \stopStaff                                               %! SM20
                                \once \override ViolaMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                \once \override ViolaMusicStaff.BarLine.bar-extent = #'(-2 . 2) %! SM20
                                R1 * 1/4
                                
                            }
                        }
                    >>
                    \tag Cello                                                           %! ST4
                    \context CelloStaffGroup = "CelloStaffGroup" <<
                        \context CelloRHMusicStaff = "CelloRHMusicStaff" {
                            \context CelloRHMusicVoice = "CelloRHMusicVoice" {
                                
                                % CelloRHMusicVoice [measure 1]                          %! SM4
                                \stopStaff                                               %! EXPLICIT_STAFF_LINES:SM8
                                \once \override CelloRHMusicStaff.StaffSymbol.line-count = 1 %! EXPLICIT_STAFF_LINES:SM8
                                \startStaff                                              %! EXPLICIT_STAFF_LINES:SM8
                                \set CelloRHMusicStaff.forceClef = ##t                   %! DEFAULT_CLEF:SM8
                                \clef "percussion"                                       %! DEFAULT_CLEF:SM8
                                \once \override CelloRHMusicStaff.Clef.color = #(x11-color 'DarkViolet) %! DEFAULT_CLEF_COLOR:SM6
                            %@% \override CelloRHMusicStaff.Clef.color = ##f             %! DEFAULT_CLEF_COLOR_CANCELLATION:SM7
                                \once \override CelloRHMusicStaff.StaffSymbol.color = #(x11-color 'blue) %! EXPLICIT_STAFF_LINES_COLOR:SM6
                                R1 * 7/4
                                \override CelloRHMusicStaff.Clef.color = #(x11-color 'violet) %! DEFAULT_CLEF_REDRAW_COLOR:SM6
                                
                                % CelloRHMusicVoice [measure 2]                          %! SM4
                                \stopStaff                                               %! SM20
                                \once \override CelloRHMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                R1 * 1/4
                                
                            }
                        }
                        \context CelloMusicStaff = "CelloMusicStaff" {
                            \context CelloMusicVoice = "CelloMusicVoice" {
                                
                                % CelloMusicVoice [measure 1]                            %! SM4
                                \once \override NoteHead.style = #'harmonic              %! OC
                                \set CelloStaffGroup.instrumentName = \markup {          %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! DEFAULT_INSTRUMENT:SM8
                                        Cello                                            %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set CelloStaffGroup.shortInstrumentName = \markup {     %! DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! DEFAULT_INSTRUMENT:SM8
                                        Vc.                                              %! DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! DEFAULT_INSTRUMENT:SM8
                                \set CelloMusicStaff.forceClef = ##t                     %! EXPLICIT_CLEF:SM8
                                \clef "treble"                                           %! EXPLICIT_CLEF:SM8
                                \once \override CelloStaffGroup.InstrumentName.color = #(x11-color 'DarkViolet) %! DEFAULT_INSTRUMENT_COLOR:SM6
                                \once \override CelloMusicStaff.Clef.color = #(x11-color 'blue) %! EXPLICIT_CLEF_COLOR:SM6
                            %@% \override CelloMusicStaff.Clef.color = ##f               %! EXPLICIT_CLEF_COLOR_CANCELLATION:SM7
                                \once \override CelloMusicVoice.DynamicText.color = #(x11-color 'blue) %! EXPLICIT_DYNAMIC_COLOR:SM6
                                fqf''1..
                                -\laissezVibrer                                          %! IC
                                \sfz                                                     %! EXPLICIT_DYNAMIC:SM8
                                ^ \markup {
                                    \column
                                        {
                                        %@% \line                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     {                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             (“Cello”                         %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \vcenter                             %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             \hcenter-in                      %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 #16                          %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 Cello                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%         \concat                              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             {                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         #10                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                         Vc.                  %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                 \vcenter                     %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%                     )                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%             }                                %! DEFAULT_INSTRUMENT_ALERT:SM10
                                        %@%     }                                        %! DEFAULT_INSTRUMENT_ALERT:SM10
                                            \line                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                {                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                    \with-color                          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        #(x11-color 'DarkViolet)         %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        {                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                (“Cello”                 %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \vcenter                     %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                \hcenter-in              %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    #16                  %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    Cello                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                            \concat                      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                {                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        \hcenter-in      %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            #10          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                            Vc.          %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                    \vcenter             %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                        )                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                                }                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                        }                                %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                                }                                        %! DEFAULT_INSTRUMENT_ALERT_WITH_COLOR:SM11
                                            \line                                        %! IC
                                                {                                        %! IC
                                                    \whiteout                            %! IC
                                                        \upright                         %! IC
                                                            pizz.                        %! IC
                                                }                                        %! IC
                                        }
                                    }
                                _ \markup {                                              %! IC
                                    \whiteout                                            %! IC
                                        \upright                                         %! IC
                                            III                                          %! IC
                                    }                                                    %! IC
                                \set CelloStaffGroup.instrumentName = \markup {          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #16                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Cello                                            %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \set CelloStaffGroup.shortInstrumentName = \markup {     %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    \hcenter-in                                          %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        #10                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                        Vc.                                              %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                    }                                                    %! REDRAWN_DEFAULT_INSTRUMENT:SM8
                                \override CelloStaffGroup.InstrumentName.color = #(x11-color 'violet) %! REDRAWN_DEFAULT_INSTRUMENT_COLOR:SM6
                                \override CelloMusicStaff.Clef.color = #(x11-color 'DeepSkyBlue2) %! EXPLICIT_CLEF_REDRAW_COLOR:SM6
                                
                                % CelloMusicVoice [measure 2]                            %! SM4
                                \stopStaff                                               %! SM20
                                \once \override CelloMusicStaff.StaffSymbol.line-count = 0 %! SM20
                                \startStaff                                              %! SM20
                                \once \override CelloMusicStaff.BarLine.bar-extent = #'(-2 . 2) %! SM20
                                R1 * 1/4
                                
                            }
                        }
                    >>
                >>
            }
        >>
    >>
}
