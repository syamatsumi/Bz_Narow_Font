@echo off
setlocal

set sz="C:\Program Files\7-Zip\7z.exe"
set input_dir=%~dp0
set output_dir=%~dp0
set options=-tzip -mx9

%sz% a "%output_dir%Bzなろうゴシック.zip" "%input_dir%\Bzなろうゴシック\" %options%
%sz% a "%output_dir%Bzなろう明朝.zip" "%input_dir%\Bzなろう明朝\" %options%

pause
