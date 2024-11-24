@echo off

rem 変数にパスを設定
set FONTFORGE="C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
set INPUTDIR=.\0_Source\BIZ_UDseriesOFL
set SCR=".\1_Scripts\scr_BIZudTF.py"

rem startコマンドで並列実行
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Regular.ttf" BIZUDMincho_SemiCond-Regular 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Regular.ttf" BIZUDMincho_ExtraCond-Regular 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Regular.ttf" BIZUDMincho_UltraCond-Regular 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Bold.ttf" BIZUDMincho_SemiCond-Bold 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Bold.ttf" BIZUDMincho_ExtraCond-Bold 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDMincho-Bold.ttf" BIZUDMincho_UltraCond-Bold 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Regular.ttf" BIZUDPMincho_SemiCond-Regular 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Regular.ttf" BIZUDPMincho_ExtraCond-Regular 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Regular.ttf" BIZUDPMincho_UltraCond-Regular 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Bold.ttf" BIZUDPMincho_SemiCond-Bold 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Bold.ttf" BIZUDPMincho_ExtraCond-Bold 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPMincho-Bold.ttf" BIZUDPMincho_UltraCond-Bold 80 0.5

Pause
