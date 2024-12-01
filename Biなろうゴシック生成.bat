rem 変数にパスを設定
set FONTFORGE="C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
set SCR="bi_narow.py"

echo このまま進めると6スレッド走ります。
pause
echo 本当に実行しますか？
pause

rem startコマンドで並列実行
start "" %FONTFORGE% %SCR% "MゴシR" "Biなろうゴシック90-Regular" 0.9
start "" %FONTFORGE% %SCR% "MゴシR" "Biなろうゴシック75-Regular" 0.75
start "" %FONTFORGE% %SCR% "MゴシR" "Biなろうゴシック50-Regular" 0.5

start "" %FONTFORGE% %SCR% "MゴシB" "Biなろうゴシック90-Bold" 0.9
start "" %FONTFORGE% %SCR% "MゴシB" "Biなろうゴシック75-Bold" 0.75
start "" %FONTFORGE% %SCR% "MゴシB" "Biなろうゴシック50-Bold" 0.5
