@echo off
setlocal enabledelayedexpansion

set VERSIONS=_v0.6.0.7z

set SZIP="C:\Program Files\7-Zip\7z.exe"
set SCRIPT_DIR=%~dp0
set PKG_DIR=%~dp0\temp_pkg
set OUTPUT_DIR=%~dp0\temp_archive
set OPTIONS=-t7z -mx9 -m0=lzma2 -ms=on -mfb=273 -md=256m

set SOURCE_DIR=%SCRIPT_DIR%..\processed
set TXT_DIR=%SCRIPT_DIR%\text


echo TTFの収集とTTCの作成とアーカイブを実施します。
pause
echo 実行しますか？
pause



echo TTFの収集とアーカイブ。
set TARGET_NAMEa=Bzなろうゴシック
set TARGET_NAMEb=BzなろうPゴシック
set TARGET_NAMEe=BzNarowGothic
set TARGET_NAMEj=%TARGET_NAMEa%
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLg.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo 処理完了: %TARGET_NAMEe%

echo TTFの収集とアーカイブ。
set TARGET_NAMEa=Bzなろう明朝
set TARGET_NAMEb=BzなろうP明朝
set TARGET_NAMEe=BzNarowMincho
set TARGET_NAMEj=%TARGET_NAMEa%
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLm.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo 処理完了: %TARGET_NAMEe%

echo TTFの収集とアーカイブ。
set TARGET_NAMEa=BzなろうMゴシック
set TARGET_NAMEb=BzなろうM明朝
set TARGET_NAMEe=BzNarowMonospace
set TARGET_NAMEj=Bzなろう全等幅
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLa.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo 処理完了: %TARGET_NAMEe%

pause
goto :eof

rem ファイルが大型化するに伴って上手く動かないようになっていったためボツ。
echo TTFの収集とTTCの作成、アーカイブ。
set UNITETTC=%SCRIPT_DIR%..\application\unitettc\unitettc64.exe

set TTC_DIR=BzなろうゴシックTTC
set TTC_DIRe=BzNarowGothicTTC
set TARGET_NAMES=Bzなろうゴシック BzなろうPゴシック BzなろうMゴシック
REM 各ターゲットをフォルダに収める
for %%T in (%TARGET_NAMES%) do (
    set TARGET_NAME=%%T
    set DEST_DIR=%PKG_DIR%\%TTC_DIR%\!TARGET_NAME!
    echo 各ターゲットをフォルダを作成する
    if not exist !DEST_DIR! mkdir !DEST_DIR!
    rem 作ったフォルダにソースフォルダから対象をコピーしてくる 
    for %%F in ("%SOURCE_DIR%\!TARGET_NAME!*.ttf") do copy "%%F" "!DEST_DIR!"
    rem ファイルリストを初期化、集めたファイルをリスト化、UNITETTCを実行
    set FILE_LIST=
    for %%F in ("!DEST_DIR!\*.*") do set FILE_LIST=!FILE_LIST! "%%F"
    call %UNITETTC% !DEST_DIR!.ttc !FILE_LIST!
    echo.
    rd /s /q "!DEST_DIR!"
    )
copy "%TXT_DIR%\OFLa.txt" "%TTC_DIR%\OFL.txt"
rem %SZIP% a "%OUTPUT_DIR%\%TTC_DIRe%%versions%" "%PKG_DIR%\%TTC_DIR%\" %OPTIONS%
echo 処理完了: %TTC_DIR%

set TTC_DIR=Bzなろう明朝TTC
set TTC_DIRe=BzNarowMinchoTTC
set TARGET_NAMES=Bzなろう明朝 BzなろうP明朝 BzなろうM明朝
REM 各ターゲットをフォルダに収める
for %%T in (%TARGET_NAMES%) do (
    set TARGET_NAME=%%T
    set DEST_DIR=%PKG_DIR%\%TTC_DIR%\!TARGET_NAME!
    echo 各ターゲットをフォルダを作成する
    if not exist !DEST_DIR! mkdir !DEST_DIR!
    rem 作ったフォルダにソースフォルダから対象をコピーしてくる 
    for %%F in ("%SOURCE_DIR%\!TARGET_NAME!*.ttf") do copy "%%F" "!DEST_DIR!"
    rem ファイルリストを初期化、集めたファイルをリスト化、UNITETTCを実行
    set FILE_LIST=
    for %%F in ("!DEST_DIR!\*.*") do set FILE_LIST=!FILE_LIST! "%%F"
    call %UNITETTC% !DEST_DIR!.ttc !FILE_LIST!
    echo.
    rd /s /q "!DEST_DIR!"
    )
copy "%TXT_DIR%\OFLa.txt" "%TTC_DIR%\OFL.txt"
rem %SZIP% a "%OUTPUT_DIR%\%TTC_DIRe%%versions%" "%PKG_DIR%\%TTC_DIR%\" %OPTIONS%
echo 処理完了: %TTC_DIR%

pause


