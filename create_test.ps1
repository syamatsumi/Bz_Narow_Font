# 実行ファイル
$scriptname = "bz_narow_core"

# 拡張子を追加してファイル名を作成
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


& $ffpy $scr MゴシB testG 0.3 M Mu uni509C ampersand uni614B uniFF36 uni3085 uni2176 uni2177 dagger
#& $ffpy $scr PミンB testM 0.9 M Mu uni509C ampersand uni614B uniFF36 uni3085 uni2176 uni2177 dagger
