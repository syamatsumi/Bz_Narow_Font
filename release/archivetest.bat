@echo off
setlocal enabledelayedexpansion

set VERSIONS=_v0.2.4.zip

set SZIP="C:\Program Files\7-Zip\7z.exe"
set SCRIPT_DIR=%~dp0
set PKG_DIR=%~dp0\temp_pkg
set OUTPUT_DIR=%~dp0
set OPTIONS=-tzip -mx9
set UNITETTC=%SCRIPT_DIR%..\application\unitettc\unitettc64.exe
set SOURCE_DIR=%SCRIPT_DIR%..\processed
set TXT_DIR=%SCRIPT_DIR%\text


echo TTFの収集とTTCの作成とアーカイブを実施します。
pause
echo 実行しますか？
pause

set TTC_DIR=Bzなろう明朝TTC
set TTC_DIRe=BzNarowMinchoTTC
set TARGET_NAMES=Bzなろう明朝 BzなろうP明朝 BzなろうM明朝
REM 各ターゲットをフォルダに収める
for %%T in (%TARGET_NAMES%) do (
    set TARGET_NAME=%%T
    set DEST_DIR=%PKG_DIR%\%TTC_DIR%\!TARGET_NAME!
    echo 各ターゲットをフォルダを作成する
    if not exist !DEST_DIR! mkdir !DEST_DIR!
    pause
    rem 作ったフォルダにソースフォルダから対象をコピーしてくる 
    for %%F in ("%SOURCE_DIR%\!TARGET_NAME!*.ttf") do copy "%%F" "!DEST_DIR!"
    pause
    rem ファイルリストを初期化、集めたファイルをリスト化、UNITETTCを実行
    set FILE_LIST=
    for %%F in ("!DEST_DIR!\*.*") do set FILE_LIST=!FILE_LIST! "%%F"
    call %UNITETTC% !DEST_DIR!.ttc !FILE_LIST!
    pause

)
copy "%TXT_DIR%\OFLa.txt" "%TTC_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TTC_DIRe%%versions%" "%PKG_DIR%\%TTC_DIR%\" %OPTIONS%
echo 処理完了: %TTC_DIR%

pause
