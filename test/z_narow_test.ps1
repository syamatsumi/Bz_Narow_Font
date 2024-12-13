$iniFile = "bz_narow.ini"
$config = @{}
Get-Content $iniFile | ForEach-Object {
    if ($_ -match '^([^#;]+)=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $config[$key] = $value
}   }
$scr = "z_narow.py"
$ffpy = $($config['ffpy'])
$ffscr = $($config['ffscr'])


& $ffpy $scr MミンB test 0.3 uni3085
#& $ffpy $scr PゴシB BzなろうPゴシック30-Bold 0.3
#& $ffpy $scr PミンR BzなろうP明朝30-Regular 0.3
#& $ffpy $scr PミンB BzなろうP明朝30-Bold 0.3