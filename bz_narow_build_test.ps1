pause
# 実行ファイル
$scriptname = "bz_narow_core"
$scriptfullname = "{0}.py" -f $scriptname

# 最大同時実行数
$maxParallel = 9

# 実行するコマンドのリスト
$commands = @(
"MゴシB BzなろうMゴシック100-Bold 1.0",
"MゴシR BzなろうMゴシック100-Regular 1.0",
"MミンB BzなろうM明朝100-Bold 1.0",
"MミンR BzなろうM明朝100-Regular 1.0",
"PゴシB BzなろうPゴシック100-Bold 1.0",
"PゴシR BzなろうPゴシック100-Regular 1.0",
"PミンB BzなろうP明朝100-Bold 1.0",
"PミンR BzなろうP明朝100-Regular 1.0",
"ゴシB Bzなろうゴシック100-Bold 1.0",
"ゴシR Bzなろうゴシック100-Regular 1.0",
"ミンB Bzなろう明朝100-Bold 1.0",
"ミンR Bzなろう明朝100-Regular 1.0"
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