@echo off
setlocal enabledelayedexpansion

set VERSIONS=_v0.2.2.zip

set SZIP="C:\Program Files\7-Zip\7z.exe"
set SCRIPT_DIR=%~dp0
set PKG_DIR=%~dp0\temp_pkg
set OUTPUT_DIR=%~dp0
set OPTIONS=-tzip -mx9
set UNITETTC=%SCRIPT_DIR%..\application\unitettc\unitettc64.exe
set SOURCE_DIR=%SCRIPT_DIR%..\processed
set TXT_DIR=%SCRIPT_DIR%\text


set TTC_DIR=Bz�Ȃ낤TTC
set TTC_DIRe=BzNarowTTC
set TARGET_NAMES=Bz�Ȃ낤�S�V�b�N Bz�Ȃ낤P�S�V�b�N Bz�Ȃ낤���� Bz�Ȃ낤P����

echo TTF�̎��W��TTC�̍쐬�ƃA�[�J�C�u�����{���܂��B
pause
echo ���s���܂����H
pause

echo M�S�V�b�N�̕��荞�ݐ�
set 

echo TTF�̎��W�ƃA�[�J�C�u�B
set TARGET_NAMEa=Bz�Ȃ낤�S�V�b�N
set TARGET_NAMEb=Bz�Ȃ낤P�S�V�b�N
set TARGET_NAMEe=BzNarowGothic
set TARGET_NAMEj=%TARGET_NAMEa%
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLg.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo ��������: %TARGET_NAMEe%

echo TTF�̎��W�ƃA�[�J�C�u�B
set TARGET_NAMEa=Bz�Ȃ낤����
set TARGET_NAMEb=Bz�Ȃ낤P����
set TARGET_NAMEe=BzNarowMincho
set TARGET_NAMEj=%TARGET_NAMEa%
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLg.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo ��������: %TARGET_NAMEe%

echo TTF�̎��W�ƃA�[�J�C�u�B
set TARGET_NAMEa=Bz�Ȃ낤M�S�V�b�N
set TARGET_NAMEb=Bz�Ȃ낤M����
set TARGET_NAMEe=BzNarowMonospace
set TARGET_NAMEj=Bz�Ȃ낤�S����
set DEST_DIR=%PKG_DIR%\%TARGET_NAMEj%
if not exist !DEST_DIR! mkdir !DEST_DIR!
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEa%*.ttf") do copy "%%F" "!DEST_DIR!"
for %%F in ("%SOURCE_DIR%\%TARGET_NAMEb%*.ttf") do copy "%%F" "!DEST_DIR!"
copy "%TXT_DIR%\OFLg.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TARGET_NAMEe%%versions%" "%PKG_DIR%\%TARGET_NAMEj%" %OPTIONS%
echo ��������: %TARGET_NAMEe%



echo TTF�̎��W��TTC�̍쐬�A�A�[�J�C�u�B
REM �e�^�[�Q�b�g���t�H���_�Ɏ��߂�
for %%T in (%TARGET_NAMES%) do (
    set TARGET_NAME=%%T
    set DEST_DIR=%PKG_DIR%\%TTC_DIR%\!TARGET_NAME!
    rem �e�^�[�Q�b�g���t�H���_���쐬����
    if not exist !DEST_DIR! mkdir !DEST_DIR!
    rem ������t�H���_�Ƀ\�[�X�t�H���_����Ώۂ��R�s�[���Ă��� 
    for %%F in ("%SOURCE_DIR%\!TARGET_NAME!*.ttf") do copy "%%F" "!DEST_DIR!"
    rem �t�@�C�����X�g���������A�W�߂��t�@�C�������X�g���AUNITETTC�����s
    set FILE_LIST=
    for %%F in ("!DEST_DIR!\*.*") do set FILE_LIST=!FILE_LIST! "%%F"
    call %UNITETTC% !DEST_DIR!.ttc !FILE_LIST!
    rd /s /q "!DEST_DIR!"
)
copy "%TXT_DIR%\OFLa.txt" "%DEST_DIR%\OFL.txt"
%SZIP% a "%OUTPUT_DIR%\%TTC_DIRe%%versions%" "%PKG_DIR%\%TTC_DIR%\" %OPTIONS%
echo ��������: %TTC_DIR%

pause