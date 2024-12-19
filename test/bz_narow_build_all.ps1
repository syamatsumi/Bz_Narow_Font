pause
# 実行するコマンドのリスト
$commands = @(
"MゴシB BzなろうMゴシック20-Bold 0.2",
"MゴシR BzなろうMゴシック20-Regular 0.2",
"MゴシB BzなろうMゴシック30-Bold 0.3",
"MゴシR BzなろうMゴシック30-Regular 0.3",
"MゴシB BzなろうMゴシック40-Bold 0.4",
"MゴシR BzなろうMゴシック40-Regular 0.4",
"MゴシB BzなろうMゴシック50-Bold 0.5",
"MゴシR BzなろうMゴシック50-Regular 0.5",
"MゴシB BzなろうMゴシック60-Bold 0.6",
"MゴシR BzなろうMゴシック60-Regular 0.6",
"MゴシB BzなろうMゴシック70-Bold 0.7",
"MゴシR BzなろうMゴシック70-Regular 0.7",
"MゴシB BzなろうMゴシック80-Bold 0.8",
"MゴシR BzなろうMゴシック80-Regular 0.8",
"MゴシB BzなろうMゴシック90-Bold 0.9",
"MゴシR BzなろうMゴシック90-Regular 0.9",
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
"PゴシB BzなろうPゴシック20-Bold 0.2",
"PゴシR BzなろうPゴシック20-Regular 0.2",
"PゴシB BzなろうPゴシック30-Bold 0.3",
"PゴシR BzなろうPゴシック30-Regular 0.3",
"PゴシB BzなろうPゴシック40-Bold 0.4",
"PゴシR BzなろうPゴシック40-Regular 0.4",
"PゴシB BzなろうPゴシック50-Bold 0.5",
"PゴシR BzなろうPゴシック50-Regular 0.5",
"PゴシB BzなろうPゴシック60-Bold 0.6",
"PゴシR BzなろうPゴシック60-Regular 0.6",
"PゴシB BzなろうPゴシック70-Bold 0.7",
"PゴシR BzなろうPゴシック70-Regular 0.7",
"PゴシB BzなろうPゴシック80-Bold 0.8",
"PゴシR BzなろうPゴシック80-Regular 0.8",
"PゴシB BzなろうPゴシック90-Bold 0.9",
"PゴシR BzなろうPゴシック90-Regular 0.9",
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
"ゴシB Bzなろうゴシック40-Bold 0.4",
"ゴシR Bzなろうゴシック40-Regular 0.4",
"ゴシB Bzなろうゴシック50-Bold 0.5",
"ゴシR Bzなろうゴシック50-Regular 0.5",
"ゴシB Bzなろうゴシック60-Bold 0.6",
"ゴシR Bzなろうゴシック60-Regular 0.6",
"ゴシB Bzなろうゴシック70-Bold 0.7",
"ゴシR Bzなろうゴシック70-Regular 0.7",
"ゴシB Bzなろうゴシック80-Bold 0.8",
"ゴシR Bzなろうゴシック80-Regular 0.8",
"ゴシB Bzなろうゴシック90-Bold 0.9",
"ゴシR Bzなろうゴシック90-Regular 0.9",
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

# 実行ファイル
$scriptname = "bz_narow_core"

# 拡張子を追加してファイル名を作成
$scriptfullname = "{0}.py" -f $scriptname
$iniFile = "{0}.ini" -f $scriptname

# 最大同時実行数
$maxParallel = 14

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

    $config = @{}
    Get-Content $iniFile | ForEach-Object {
        if ($_ -match '^([^#;]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $config[$key] = $value
    }   }
    $ffpy = $($config['ffpy'])
    $build_dir = $($config['Build_Fonts_Dir'])

    # フォルダが存在しない場合は作成する
    if (-not (Test-Path -Path $build_dir)) {
        New-Item -Path $build_dir -ItemType Directory | Out-Null
        Write-Host "Created directory: $build_dir"
    }

    # コマンドを実行
    $CommandLine = @($scriptfullname) + $args
    Write-Host "Executing: $ffpy $scriptfullname $args"
    $logFile = "$build_dir\$($args[1])_stdout.err"  # 引数3を抽出してログファイル名を生成
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