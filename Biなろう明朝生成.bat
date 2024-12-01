rem 変数にパスを設定
set FONTFORGE="C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
set SCR="bi_narow.py"

echo このまま進めると6スレッド走ります。
pause
echo 本当に実行しますか？
pause

rem startコマンドで並列実行
start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝90-Regular" 0.9
start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝75-Regular" 0.75
start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝50-Regular" 0.5

start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝90-Bold" 0.9
start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝75-Bold" 0.75
start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝50-Bold" 0.5
