pause
# 実行するコマンドのリスト
$commands = @(
"bz_narow.py MゴシB BzなろうMゴシック30-Bold 0.3",
"bz_narow.py MゴシR BzなろうMゴシック30-Regular 0.3",
"bz_narow.py MゴシB BzなろうMゴシック40-Bold 0.4",
"bz_narow.py MゴシR BzなろうMゴシック40-Regular 0.4",
"bz_narow.py MゴシB BzなろうMゴシック50-Bold 0.5",
"bz_narow.py MゴシR BzなろうMゴシック50-Regular 0.5",
"bz_narow.py MゴシB BzなろうMゴシック60-Bold 0.6",
"bz_narow.py MゴシR BzなろうMゴシック60-Regular 0.6",
"bz_narow.py MゴシB BzなろうMゴシック70-Bold 0.7",
"bz_narow.py MゴシR BzなろうMゴシック70-Regular 0.7",
"bz_narow.py MゴシB BzなろうMゴシック80-Bold 0.8",
"bz_narow.py MゴシR BzなろうMゴシック80-Regular 0.8",
"bz_narow.py MゴシB BzなろうMゴシック90-Bold 0.9",
"bz_narow.py MゴシR BzなろうMゴシック90-Regular 0.9",
"bz_narow.py MミンB BzなろうM明朝30-Bold 0.3",
"bz_narow.py MミンR BzなろうM明朝30-Regular 0.3",
"bz_narow.py MミンB BzなろうM明朝40-Bold 0.4",
"bz_narow.py MミンR BzなろうM明朝40-Regular 0.4",
"bz_narow.py MミンB BzなろうM明朝50-Bold 0.5",
"bz_narow.py MミンR BzなろうM明朝50-Regular 0.5",
"bz_narow.py MミンB BzなろうM明朝60-Bold 0.6",
"bz_narow.py MミンR BzなろうM明朝60-Regular 0.6",
"bz_narow.py MミンB BzなろうM明朝70-Bold 0.7",
"bz_narow.py MミンR BzなろうM明朝70-Regular 0.7",
"bz_narow.py MミンB BzなろうM明朝80-Bold 0.8",
"bz_narow.py MミンR BzなろうM明朝80-Regular 0.8",
"bz_narow.py MミンB BzなろうM明朝90-Bold 0.9",
"bz_narow.py MミンR BzなろうM明朝90-Regular 0.9",
"bz_narow.py PゴシB BzなろうPゴシック30-Bold 0.3",
"bz_narow.py PゴシR BzなろうPゴシック30-Regular 0.3",
"bz_narow.py PゴシB BzなろうPゴシック40-Bold 0.4",
"bz_narow.py PゴシR BzなろうPゴシック40-Regular 0.4",
"bz_narow.py PゴシB BzなろうPゴシック50-Bold 0.5",
"bz_narow.py PゴシR BzなろうPゴシック50-Regular 0.5",
"bz_narow.py PゴシB BzなろうPゴシック60-Bold 0.6",
"bz_narow.py PゴシR BzなろうPゴシック60-Regular 0.6",
"bz_narow.py PゴシB BzなろうPゴシック70-Bold 0.7",
"bz_narow.py PゴシR BzなろうPゴシック70-Regular 0.7",
"bz_narow.py PゴシB BzなろうPゴシック80-Bold 0.8",
"bz_narow.py PゴシR BzなろうPゴシック80-Regular 0.8",
"bz_narow.py PゴシB BzなろうPゴシック90-Bold 0.9",
"bz_narow.py PゴシR BzなろうPゴシック90-Regular 0.9",
"bz_narow.py PミンB BzなろうP明朝30-Bold 0.3",
"bz_narow.py PミンR BzなろうP明朝30-Regular 0.3",
"bz_narow.py PミンB BzなろうP明朝40-Bold 0.4",
"bz_narow.py PミンR BzなろうP明朝40-Regular 0.4",
"bz_narow.py PミンB BzなろうP明朝50-Bold 0.5",
"bz_narow.py PミンR BzなろうP明朝50-Regular 0.5",
"bz_narow.py PミンB BzなろうP明朝60-Bold 0.6",
"bz_narow.py PミンR BzなろうP明朝60-Regular 0.6",
"bz_narow.py PミンB BzなろうP明朝70-Bold 0.7",
"bz_narow.py PミンR BzなろうP明朝70-Regular 0.7",
"bz_narow.py PミンB BzなろうP明朝80-Bold 0.8",
"bz_narow.py PミンR BzなろうP明朝80-Regular 0.8",
"bz_narow.py PミンB BzなろうP明朝90-Bold 0.9",
"bz_narow.py PミンR BzなろうP明朝90-Regular 0.9",
"bz_narow.py ゴシB Bzなろうゴシック50-Bold 0.5",
"bz_narow.py ゴシR Bzなろうゴシック50-Regular 0.5",
"bz_narow.py ゴシB Bzなろうゴシック60-Bold 0.6",
"bz_narow.py ゴシR Bzなろうゴシック60-Regular 0.6",
"bz_narow.py ゴシB Bzなろうゴシック70-Bold 0.7",
"bz_narow.py ゴシR Bzなろうゴシック70-Regular 0.7",
"bz_narow.py ゴシB Bzなろうゴシック80-Bold 0.8",
"bz_narow.py ゴシR Bzなろうゴシック80-Regular 0.8",
"bz_narow.py ゴシB Bzなろうゴシック90-Bold 0.9",
"bz_narow.py ゴシR Bzなろうゴシック90-Regular 0.9",
"bz_narow.py ミンB Bzなろう明朝50-Bold 0.5",
"bz_narow.py ミンR Bzなろう明朝50-Regular 0.5",
"bz_narow.py ミンB Bzなろう明朝60-Bold 0.6",
"bz_narow.py ミンR Bzなろう明朝60-Regular 0.6",
"bz_narow.py ミンB Bzなろう明朝70-Bold 0.7",
"bz_narow.py ミンR Bzなろう明朝70-Regular 0.7",
"bz_narow.py ミンB Bzなろう明朝80-Bold 0.8",
"bz_narow.py ミンR Bzなろう明朝80-Regular 0.8",
"bz_narow.py ミンB Bzなろう明朝90-Bold 0.9",
"bz_narow.py ミンR Bzなろう明朝90-Regular 0.9"
)

# 最大同時実行数
$maxParallel = 12

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

    $iniFile = "bz_narow.ini"
    $config = @{}
    Get-Content $iniFile | ForEach-Object {
        if ($_ -match '^([^#;]+)=(.+)$') {
            $key = $matches[1].Trim()
            $value = $matches[2].Trim()
            $config[$key] = $value
    }   }
    $ffpy = $($config['ffpy'])

    # コマンドを実行
    Write-Host "Executing: $ffpy $args"
    $logFile = "processlog\$($args[2])_stderr.log"  # 引数3を抽出してログファイル名を生成
    try {
        $process = Start-Process -FilePath $ffpy `
            -ArgumentList $args `
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