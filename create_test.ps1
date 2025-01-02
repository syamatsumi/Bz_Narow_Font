# ���s�t�@�C��
$scriptname = "bz_narow_ttfconv"
$scr = "{0}.py" -f $scriptname

# ���s�t�@�C���Ō�̃A���_�[�o�[�O����s�b�N�A�b�v
if ($scriptname -match "^(.*)_(.*)$") {
    $scr_prefix = $matches[1]
    $scr_suffix = $matches[2]
    $iniFile = "{0}_{1}.ini" -f $scr_prefix, "settings"
} else {
    # �A���_�[�o�[���Ȃ���΂��̂܂�
    $iniFile = "{0}.ini" -f $scriptname
    $scr_suffix = $scriptname
}

$config = @{}
Get-Content $iniFile | ForEach-Object {
    if ($_ -match '^([^#;]+)=(.+)$') {
        $key = $matches[1].Trim()
        $value = $matches[2].Trim()
        $config[$key] = $value
}   }
$ffpy = $($config['ffpy'])
$ffscr = $($config['ffscr'])
$build_dir = $($config['Build_Fonts_Dir'])

# �t�H���_�����݂��Ȃ��ꍇ�͍쐬����
if (-not (Test-Path -Path $build_dir)) {
    New-Item -Path $build_dir -ItemType Directory | Out-Null
    Write-Host "Created directory: $build_dir"
}

& $ffpy $scr M�S�VB Bz�Ȃ낤M�S�V�b�N100-Bold 1.0
#& $ffpy $scr M�~��B test 0.5
#& $ffpy $scr P�S�VB testG 0.9 uni9A19 uni890A uni99F2 uni9B4E uni95E2
#& $ffpy $scr M�S�VB testG 0.3 M Mu uni3050 uni509C ampersand uni614B uniFF36 uni3085 uni2176 uni2177 dagger
#& $ffpy $scr P�~��B testM 0.9 M Mu uni509C ampersand uni614B uniFF36 uni3085 uni2176 uni2177 dagger
