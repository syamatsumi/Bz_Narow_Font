# FontForgeÇé¿çs
$fontforge = "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"
$inputDir = ".\0_Source\Inconsolata\ttf"
$scr1 = ".\1_scripts\scr_InconsolataTFMono.py"
$scr2 = ".\1_scripts\scr_InconsolataTFProp.py"

& $fontforge $scr1 "$inputDir\Inconsolata-SemiCondensed.ttf" "Inconsolata_SemiCond-Regular" 922
& $fontforge $scr1 "$inputDir\Inconsolata-ExtraCondensed.ttf" "Inconsolata_ExtraCond-Regular" 768
& $fontforge $scr1 "$inputDir\Inconsolata-UltraCondensed.ttf" "Inconsolata_UltraCond-Regular" 512
& $fontforge $scr1 "$inputDir\Inconsolata-SemiCondensedBold.ttf" "Inconsolata_SemiCond-Bold" 922
& $fontforge $scr1 "$inputDir\Inconsolata-ExtraCondensedBold.ttf" "Inconsolata_ExtraCond-Bold" 768
& $fontforge $scr1 "$inputDir\Inconsolata-UltraCondensedBold.ttf" "Inconsolata_UltraCond-Bold" 512

& $fontforge $scr2 "$inputDir\Inconsolata-SemiCondensed.ttf" "InconsolataP_SemiCond-Regular" 922
& $fontforge $scr2 "$inputDir\Inconsolata-ExtraCondensed.ttf" "InconsolataP_ExtraCond-Regular" 768
& $fontforge $scr2 "$inputDir\Inconsolata-UltraCondensed.ttf" "InconsolataP_UltraCond-Regular" 512
& $fontforge $scr2 "$inputDir\Inconsolata-SemiCondensedBold.ttf" "InconsolataP_SemiCond-Bold" 922
& $fontforge $scr2 "$inputDir\Inconsolata-ExtraCondensedBold.ttf" "InconsolataP_ExtraCond-Bold" 768
& $fontforge $scr2 "$inputDir\Inconsolata-UltraCondensedBold.ttf" "InconsolataP_UltraCond-Bold" 512
