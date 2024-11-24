@echo off

rem 変数にパスを設定
set FONTFORGE="C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
set INPUTDIR=.\0_Source\BIZ_UDseriesOFL
set SCR=".\1_Scripts\scr_BIZudTF.py"

rem startコマンドで並列実行
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Regular.ttf" BIZUDGothic_SemiCond-Regular 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Regular.ttf" BIZUDGothic_ExtraCond-Regular 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Regular.ttf" BIZUDGothic_UltraCond-Regular 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Bold.ttf" BIZUDGothic_SemiCond-Bold 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Bold.ttf" BIZUDGothic_ExtraCond-Bold 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDGothic-Bold.ttf" BIZUDGothic_UltraCond-Bold 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Regular.ttf" BIZUDPGothic_SemiCond-Regular 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Regular.ttf" BIZUDPGothic_ExtraCond-Regular 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Regular.ttf" BIZUDPGothic_UltraCond-Regular 80 0.5

start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Bold.ttf" BIZUDPGothic_SemiCond-Bold 15 0.9
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Bold.ttf" BIZUDPGothic_ExtraCond-Bold 30 0.75
start "" %FONTFORGE% %SCR% "%INPUTDIR%\BIZUDPGothic-Bold.ttf" BIZUDPGothic_UltraCond-Bold 80 0.5

Pause
