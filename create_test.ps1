# ���s�t�@�C��
$scriptname = "bz_narow_core"

# �g���q��ǉ����ăt�@�C�������쐬
$scr = "{0}.py" -f $scriptname
$iniFile = "{0}.ini" -f $scriptname

$config = @{}
Get-Content $iniFile | ForEach-Object {
    if ($_ -match '^([^#;]+)=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $config[$key] = $value
}   }
$ffpy = $($config['ffpy'])
$ffscr = $($config['ffscr'])

& $ffpy $scr M�S�VB test 0.3
#& $ffpy $scr M�S�VB test 0.3 uni509C ampersand uni614B uniFF36 uni3085 uni2176 uni2177 dagger
#& $ffpy $scr P�S�VB Bz�Ȃ낤P�S�V�b�N30-Bold 0.3
#& $ffpy $scr P�~��R Bz�Ȃ낤P����30-Regular 0.3
#& $ffpy $scr P�~��B Bz�Ȃ낤P����30-Bold 0.3 uniff36