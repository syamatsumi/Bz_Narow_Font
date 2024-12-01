rem 変数にパスを設定
set FONTFORGE="C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
set SCR="bi_narow.py"

echo このまま進めると24スレッド走ります。
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

start "" %FONTFORGE% %SCR% "PゴシR" "BiなろうPゴシック90-Regular" 0.9
start "" %FONTFORGE% %SCR% "PゴシR" "BiなろうPゴシック75-Regular" 0.75
start "" %FONTFORGE% %SCR% "PゴシR" "BiなろうPゴシック50-Regular" 0.5

start "" %FONTFORGE% %SCR% "PゴシB" "BiなろうPゴシック90-Bold" 0.9
start "" %FONTFORGE% %SCR% "PゴシB" "BiなろうPゴシック75-Bold" 0.75
start "" %FONTFORGE% %SCR% "PゴシB" "BiなろうPゴシック50-Bold" 0.5

start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝90-Regular" 0.9
start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝75-Regular" 0.75
start "" %FONTFORGE% %SCR% "MミンR" "Biなろう明朝50-Regular" 0.5

start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝90-Bold" 0.9
start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝75-Bold" 0.75
start "" %FONTFORGE% %SCR% "MミンB" "Biなろう明朝50-Bold" 0.5

start "" %FONTFORGE% %SCR% "PミンR" "BiなろうP明朝90-Regular" 0.9
start "" %FONTFORGE% %SCR% "PミンR" "BiなろうP明朝75-Regular" 0.75
start "" %FONTFORGE% %SCR% "PミンR" "BiなろうP明朝50-Regular" 0.5

start "" %FONTFORGE% %SCR% "PミンB" "BiなろうP明朝90-Bold" 0.9
start "" %FONTFORGE% %SCR% "PミンB" "BiなろうP明朝75-Bold" 0.75
start "" %FONTFORGE% %SCR% "PミンB" "BiなろうP明朝50-Bold" 0.5