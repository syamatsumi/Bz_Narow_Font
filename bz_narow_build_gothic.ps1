pause
# ���s�t�@�C��
$scriptname = "bz_narow_core"
$scriptfullname = "{0}.py" -f $scriptname

# �ő哯�����s��
$maxParallel = 7

# ���s����R�}���h�̃��X�g
$commands = @(
"M�S�VB Bz�Ȃ낤M�S�V�b�N100-Bold 1.0",
"M�S�VR Bz�Ȃ낤M�S�V�b�N100-Regular 1.0",
"M�S�VB Bz�Ȃ낤M�S�V�b�N20-Bold 0.2",
"M�S�VR Bz�Ȃ낤M�S�V�b�N20-Regular 0.2",
"M�S�VB Bz�Ȃ낤M�S�V�b�N30-Bold 0.3",
"M�S�VR Bz�Ȃ낤M�S�V�b�N30-Regular 0.3",
"M�S�VB Bz�Ȃ낤M�S�V�b�N40-Bold 0.4",
"M�S�VR Bz�Ȃ낤M�S�V�b�N40-Regular 0.4",
"M�S�VB Bz�Ȃ낤M�S�V�b�N50-Bold 0.5",
"M�S�VR Bz�Ȃ낤M�S�V�b�N50-Regular 0.5",
"M�S�VB Bz�Ȃ낤M�S�V�b�N60-Bold 0.6",
"M�S�VR Bz�Ȃ낤M�S�V�b�N60-Regular 0.6",
"M�S�VB Bz�Ȃ낤M�S�V�b�N70-Bold 0.7",
"M�S�VR Bz�Ȃ낤M�S�V�b�N70-Regular 0.7",
"M�S�VB Bz�Ȃ낤M�S�V�b�N80-Bold 0.8",
"M�S�VR Bz�Ȃ낤M�S�V�b�N80-Regular 0.8",
"M�S�VB Bz�Ȃ낤M�S�V�b�N90-Bold 0.9",
"M�S�VR Bz�Ȃ낤M�S�V�b�N90-Regular 0.9",
"P�S�VB Bz�Ȃ낤P�S�V�b�N100-Bold 1.0",
"P�S�VR Bz�Ȃ낤P�S�V�b�N100-Regular 1.0",
"P�S�VB Bz�Ȃ낤P�S�V�b�N20-Bold 0.2",
"P�S�VR Bz�Ȃ낤P�S�V�b�N20-Regular 0.2",
"P�S�VB Bz�Ȃ낤P�S�V�b�N30-Bold 0.3",
"P�S�VR Bz�Ȃ낤P�S�V�b�N30-Regular 0.3",
"P�S�VB Bz�Ȃ낤P�S�V�b�N40-Bold 0.4",
"P�S�VR Bz�Ȃ낤P�S�V�b�N40-Regular 0.4",
"P�S�VB Bz�Ȃ낤P�S�V�b�N50-Bold 0.5",
"P�S�VR Bz�Ȃ낤P�S�V�b�N50-Regular 0.5",
"P�S�VB Bz�Ȃ낤P�S�V�b�N60-Bold 0.6",
"P�S�VR Bz�Ȃ낤P�S�V�b�N60-Regular 0.6",
"P�S�VB Bz�Ȃ낤P�S�V�b�N70-Bold 0.7",
"P�S�VR Bz�Ȃ낤P�S�V�b�N70-Regular 0.7",
"P�S�VB Bz�Ȃ낤P�S�V�b�N80-Bold 0.8",
"P�S�VR Bz�Ȃ낤P�S�V�b�N80-Regular 0.8",
"P�S�VB Bz�Ȃ낤P�S�V�b�N90-Bold 0.9",
"P�S�VR Bz�Ȃ낤P�S�V�b�N90-Regular 0.9",
"�S�VB Bz�Ȃ낤�S�V�b�N100-Bold 1.0",
"�S�VR Bz�Ȃ낤�S�V�b�N100-Regular 1.0",
"�S�VB Bz�Ȃ낤�S�V�b�N40-Bold 0.4",
"�S�VR Bz�Ȃ낤�S�V�b�N40-Regular 0.4",
"�S�VB Bz�Ȃ낤�S�V�b�N50-Bold 0.5",
"�S�VR Bz�Ȃ낤�S�V�b�N50-Regular 0.5",
"�S�VB Bz�Ȃ낤�S�V�b�N60-Bold 0.6",
"�S�VR Bz�Ȃ낤�S�V�b�N60-Regular 0.6",
"�S�VB Bz�Ȃ낤�S�V�b�N70-Bold 0.7",
"�S�VR Bz�Ȃ낤�S�V�b�N70-Regular 0.7",
"�S�VB Bz�Ȃ낤�S�V�b�N80-Bold 0.8",
"�S�VR Bz�Ȃ낤�S�V�b�N80-Regular 0.8",
"�S�VB Bz�Ȃ낤�S�V�b�N90-Bold 0.9",
"�S�VR Bz�Ȃ낤�S�V�b�N90-Regular 0.9"
)

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

# ���s���̃v���Z�X���Ǘ�
$runningJobs = @()

foreach ($command in $commands) {
    # ���s���v���Z�X�������𒴂���Ȃ�ҋ@
    while ($runningJobs.Count -ge $maxParallel) {
        Start-Sleep -Seconds 3
        # ���s���̃v���Z�X�̂ݕێ�
        $runningJobs = $runningJobs | Where-Object { $_ -ne $null -and $_.HasExited -eq $false }
    }

    # �R�}���h�𕪊�
    $args = $command -split " "
    if ($args.Count -eq 0) {
        Write-Warning "�����ȃR�}���h: $command"
        continue
    }

    # �R���t�B�O�t�@�C���̓ǂݍ���
    $config = @{}
    Get-Content $iniFile | ForEach-Object {
        if ($_ -match '^([^#;]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $config[$key] = $value
    }   }
    $ffpy = $($config['ffpy'])
    $build_dir = $($config['Build_Fonts_Dir'])
    $warnlog_dir = Join-Path $build_dir "warning_log"

    # �t�H���_�����݂��Ȃ��ꍇ�͍쐬����
    if (-not (Test-Path -Path $warnlog_dir)) {
        New-Item -Path $warnlog_dir -ItemType Directory -Force | Out-Null
        Write-Host "Created directory: $warnlog_dir"
    }

    # �R�}���h�����s
    $CommandLine = @($scriptfullname) + $args
    Write-Host "Executing: $ffpy $scriptfullname $args"
    $logFile = "$warnlog_dir\$($args[1])_$scr_suffix.err"
    try {
        $process = Start-Process -FilePath $ffpy `
            -ArgumentList $CommandLine `
            -RedirectStandardError $logFile `
            -NoNewWindow `
            -PassThru `
            -ErrorAction 'Continue'
        $runningJobs += $process
    }
    catch {
        Write-Warning "Start-Process �Ɏ��s: $_"
        Write-Host "�G���[�ڍ�: $($_.Exception.Message)"
    }
}

# �v���Z�X�̏I����҂�
$runningJobs | ForEach-Object {
    try {
        if ($_ -ne $null -and $_.HasExited -eq $false) {
            $_.WaitForExit()
        }
    } catch {
        Write-Warning "�v���Z�XID $($_.Id) �̏I���ҋ@���ɃG���[���������܂���: $_"
        Write-Host "�G���[�ڍ�: $($_.Exception.Message)"
    }
}

pause