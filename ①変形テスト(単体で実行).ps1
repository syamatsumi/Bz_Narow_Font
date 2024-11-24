# FontForgeÇé¿çs
$fontforge = "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
$inputDir1 = ".\0_Source\Inconsolata\ttf"
$inputDir2 = ".\0_Source\BIZ_UDseriesOFL"
$scr1 = ".\1_scripts\scr_InconsolataTF.py"
$scr2 = ".\1_scripts\scr_InconsolataTFProp.py"
$scr3 = ".\1_scripts\scr_BIZudTF.py"


& $fontforge $scr3 "$inputDir2\BIZUDGothic-Bold.ttf" "BIZUDGothic-UCR" 80 0.5