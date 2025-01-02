pause
# 実行ファイル
$scriptname = "bz_narow_core"
$scriptfullname = "{0}.py" -f $scriptname

# 最大同時実行数
$maxParallel = 4

# 実行するコマンドのリスト
$commands = @(
"MミンB BzなろうM明朝100-Bold 1.0",
"MミンR BzなろうM明朝100-Regular 1.0",
"MミンB BzなろうM明朝20-Bold 0.2",
"MミンR BzなろうM明朝20-Regular 0.2",
"MミンB BzなろうM明朝30-Bold 0.3",
"MミンR BzなろうM明朝30-Regular 0.3",
"MミンB BzなろうM明朝40-Bold 0.4",
"MミンR BzなろうM明朝40-Regular 0.4",
"MミンB BzなろうM明朝50-Bold 0.5",
"MミンR BzなろうM明朝50-Regular 0.5",
"MミンB BzなろうM明朝60-Bold 0.6",
"MミンR BzなろうM明朝60-Regular 0.6",
"MミンB BzなろうM明朝70-Bold 0.7",
"MミンR BzなろうM明朝70-Regular 0.7",
"MミンB BzなろうM明朝80-Bold 0.8",
"MミンR BzなろうM明朝80-Regular 0.8",
"MミンB BzなろうM明朝90-Bold 0.9",
"MミンR BzなろうM明朝90-Regular 0.9",
"PミンB BzなろうP明朝100-Bold 1.0",
"PミンR BzなろうP明朝100-Regular 1.0",
"PミンB BzなろうP明朝20-Bold 0.2",
"PミンR BzなろうP明朝20-Regular 0.2",
"PミンB BzなろうP明朝30-Bold 0.3",
"PミンR BzなろうP明朝30-Regular 0.3",
"PミンB BzなろうP明朝40-Bold 0.4",
"PミンR BzなろうP明朝40-Regular 0.4",
"PミンB BzなろうP明朝50-Bold 0.5",
"PミンR BzなろうP明朝50-Regular 0.5",
"PミンB BzなろうP明朝60-Bold 0.6",
"PミンR BzなろうP明朝60-Regular 0.6",
"PミンB BzなろうP明朝70-Bold 0.7",
"PミンR BzなろうP明朝70-Regular 0.7",
"PミンB BzなろうP明朝80-Bold 0.8",
"PミンR BzなろうP明朝80-Regular 0.8",
"PミンB BzなろうP明朝90-Bold 0.9",
"PミンR BzなろうP明朝90-Regular 0.9",
"ミンB Bzなろう明朝100-Bold 1.0",
"ミンR Bzなろう明朝100-Regular 1.0",
"ミンB Bzなろう明朝40-Bold 0.4",
"ミンR Bzなろう明朝40-Regular 0.4",
"ミンB Bzなろう明朝50-Bold 0.5",
"ミンR Bzなろう明朝50-Regular 0.5",
"ミンB Bzなろう明朝60-Bold 0.6",
"ミンR Bzなろう明朝60-Regular 0.6",
"ミンB Bzなろう明朝70-Bold 0.7",
"ミンR Bzなろう明朝70-Regular 0.7",
"ミンB Bzなろう明朝80-Bold 0.8",
"ミンR Bzなろう明朝80-Regular 0.8",
"ミンB Bzなろう明朝90-Bold 0.9",
"ミンR Bzなろう明朝90-Regular 0.9"
)

# 実行ファイル最後のアンダーバー前後をピックアップ
if ($scriptname -match "^(.*)_(.*)$") {
    $scr_prefix = $matches[1]
    $scr_suffix = $matches[2]
    $iniFile = "{0}_{1}.ini" -f $scr_prefix, "settings"
} else {
    # アンダーバーがなければそのまま
    $iniFile = "{0}.ini" -f $scriptname
    $scr_suffix = $scriptname
}

# 実行中のプロセスを管理
$runningJobs = @()

foreach ($command in $commands) {
    # 実行中プロセスが制限を超えるなら待機
    while ($runningJobs.Count -ge $maxParallel) {
        Start-Sleep -Seconds 3
        # 実行中のプロセスのみ保持
        $runningJobs = $runningJobs | Where-Object { $_ -ne $null -and $_.HasExited -eq $false }
    }

    # コマンドを分割
    $args = $command -split " "
    if ($args.Count -eq 0) {
        Write-Warning "無効なコマンド: $command"
        continue
    }

    # コンフィグファイルの読み込み
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

    # フォルダが存在しない場合は作成する
    if (-not (Test-Path -Path $warnlog_dir)) {
        New-Item -Path $warnlog_dir -ItemType Directory -Force | Out-Null
        Write-Host "Created directory: $warnlog_dir"
    }

    # コマンドを実行
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
        Write-Warning "Start-Process に失敗: $_"
        Write-Host "エラー詳細: $($_.Exception.Message)"
    }
}

# プロセスの終了を待つ
$runningJobs | ForEach-Object {
    try {
        if ($_ -ne $null -and $_.HasExited -eq $false) {
            $_.WaitForExit()
        }
    } catch {
        Write-Warning "プロセスID $($_.Id) の終了待機中にエラーが発生しました: $_"
        Write-Host "エラー詳細: $($_.Exception.Message)"
    }
}

pause