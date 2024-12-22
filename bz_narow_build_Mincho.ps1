pause
# ���s����R�}���h�̃��X�g
$commands = @(
"M�~��B Bz�Ȃ낤M����20-Bold 0.2",
"M�~��R Bz�Ȃ낤M����20-Regular 0.2",
"M�~��B Bz�Ȃ낤M����30-Bold 0.3",
"M�~��R Bz�Ȃ낤M����30-Regular 0.3",
"M�~��B Bz�Ȃ낤M����40-Bold 0.4",
"M�~��R Bz�Ȃ낤M����40-Regular 0.4",
"M�~��B Bz�Ȃ낤M����50-Bold 0.5",
"M�~��R Bz�Ȃ낤M����50-Regular 0.5",
"M�~��B Bz�Ȃ낤M����60-Bold 0.6",
"M�~��R Bz�Ȃ낤M����60-Regular 0.6",
"M�~��B Bz�Ȃ낤M����70-Bold 0.7",
"M�~��R Bz�Ȃ낤M����70-Regular 0.7",
"M�~��B Bz�Ȃ낤M����80-Bold 0.8",
"M�~��R Bz�Ȃ낤M����80-Regular 0.8",
"M�~��B Bz�Ȃ낤M����90-Bold 0.9",
"M�~��R Bz�Ȃ낤M����90-Regular 0.9",
"P�~��B Bz�Ȃ낤P����20-Bold 0.2",
"P�~��R Bz�Ȃ낤P����20-Regular 0.2",
"P�~��B Bz�Ȃ낤P����30-Bold 0.3",
"P�~��R Bz�Ȃ낤P����30-Regular 0.3",
"P�~��B Bz�Ȃ낤P����40-Bold 0.4",
"P�~��R Bz�Ȃ낤P����40-Regular 0.4",
"P�~��B Bz�Ȃ낤P����50-Bold 0.5",
"P�~��R Bz�Ȃ낤P����50-Regular 0.5",
"P�~��B Bz�Ȃ낤P����60-Bold 0.6",
"P�~��R Bz�Ȃ낤P����60-Regular 0.6",
"P�~��B Bz�Ȃ낤P����70-Bold 0.7",
"P�~��R Bz�Ȃ낤P����70-Regular 0.7",
"P�~��B Bz�Ȃ낤P����80-Bold 0.8",
"P�~��R Bz�Ȃ낤P����80-Regular 0.8",
"P�~��B Bz�Ȃ낤P����90-Bold 0.9",
"P�~��R Bz�Ȃ낤P����90-Regular 0.9",
"�~��B Bz�Ȃ낤����40-Bold 0.4",
"�~��R Bz�Ȃ낤����40-Regular 0.4",
"�~��B Bz�Ȃ낤����50-Bold 0.5",
"�~��R Bz�Ȃ낤����50-Regular 0.5",
"�~��B Bz�Ȃ낤����60-Bold 0.6",
"�~��R Bz�Ȃ낤����60-Regular 0.6",
"�~��B Bz�Ȃ낤����70-Bold 0.7",
"�~��R Bz�Ȃ낤����70-Regular 0.7",
"�~��B Bz�Ȃ낤����80-Bold 0.8",
"�~��R Bz�Ȃ낤����80-Regular 0.8",
"�~��B Bz�Ȃ낤����90-Bold 0.9",
"�~��R Bz�Ȃ낤����90-Regular 0.9"
)

# ���s�t�@�C��
$scriptname = "bz_narow_core"

# �g���q��ǉ����ăt�@�C�������쐬
$scriptfullname = "{0}.py" -f $scriptname
$iniFile = "{0}.ini" -f $scriptname

# �ő哯�����s��
$maxParallel = 9

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

    $config = @{}
    Get-Content $iniFile | ForEach-Object {
        if ($_ -match '^([^#;]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $config[$key] = $value
    }   }
    $ffpy = $($config['ffpy'])
    $build_dir = $($config['Build_Fonts_Dir'])

    # �t�H���_�����݂��Ȃ��ꍇ�͍쐬����
    if (-not (Test-Path -Path $build_dir)) {
        New-Item -Path $build_dir -ItemType Directory | Out-Null
        Write-Host "Created directory: $build_dir"
    }

    # �R�}���h�����s
    $CommandLine = @($scriptfullname) + $args
    Write-Host "Executing: $ffpy $scriptfullname $args"
    $logFile = "$build_dir\$($args[1])_stdout.err"  # ����3�𒊏o���ă��O�t�@�C�����𐶐�
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