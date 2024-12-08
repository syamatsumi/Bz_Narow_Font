pause
# 実行するコマンドのリスト
$commands = @(
"bz_narow.py ゴシR Bzなろうゴシック87-Regular 0.875",
"bz_narow.py ゴシR Bzなろうゴシック75-Regular 0.75",
"bz_narow.py ゴシR Bzなろうゴシック60-Regular 0.6",
"bz_narow.py ゴシR Bzなろうゴシック50-Regular 0.5",
"bz_narow.py ゴシB Bzなろうゴシック87-Bold 0.875",
"bz_narow.py ゴシB Bzなろうゴシック75-Bold 0.75",
"bz_narow.py ゴシB Bzなろうゴシック60-Bold 0.6",
"bz_narow.py ゴシB Bzなろうゴシック50-Bold 0.5",
"bz_narow.py PゴシR BzなろうPゴシック87-Regular 0.875",
"bz_narow.py PゴシR BzなろうPゴシック75-Regular 0.75",
"bz_narow.py PゴシR BzなろうPゴシック60-Regular 0.6",
"bz_narow.py PゴシR BzなろうPゴシック50-Regular 0.5",
"bz_narow.py PゴシR BzなろうPゴシック30-Regular 0.3",
"bz_narow.py PゴシB BzなろうPゴシック87-Bold 0.875",
"bz_narow.py PゴシB BzなろうPゴシック75-Bold 0.75",
"bz_narow.py PゴシB BzなろうPゴシック60-Bold 0.6",
"bz_narow.py PゴシB BzなろうPゴシック50-Bold 0.5",
"bz_narow.py PゴシB BzなろうPゴシック30-Bold 0.3",
"bz_narow.py MゴシR BzなろうMゴシック87-Regular 0.875",
"bz_narow.py MゴシR BzなろうMゴシック75-Regular 0.75",
"bz_narow.py MゴシR BzなろうMゴシック60-Regular 0.6",
"bz_narow.py MゴシR BzなろうMゴシック50-Regular 0.5",
"bz_narow.py MゴシR BzなろうMゴシック30-Regular 0.3",
"bz_narow.py MゴシB BzなろうMゴシック87-Bold 0.875",
"bz_narow.py MゴシB BzなろうMゴシック75-Bold 0.75",
"bz_narow.py MゴシB BzなろうMゴシック60-Bold 0.6",
"bz_narow.py MゴシB BzなろうMゴシック50-Bold 0.5",
"bz_narow.py MゴシB BzなろうMゴシック30-Bold 0.3",
"bz_narow.py ミンR Bzなろう明朝87-Regular 0.875",
"bz_narow.py ミンR Bzなろう明朝75-Regular 0.75",
"bz_narow.py ミンR Bzなろう明朝60-Regular 0.6",
"bz_narow.py ミンR Bzなろう明朝50-Regular 0.5",
"bz_narow.py ミンB Bzなろう明朝87-Bold 0.875",
"bz_narow.py ミンB Bzなろう明朝75-Bold 0.75",
"bz_narow.py ミンB Bzなろう明朝60-Bold 0.6",
"bz_narow.py ミンB Bzなろう明朝50-Bold 0.5",
"bz_narow.py PミンR BzなろうP明朝87-Regular 0.875",
"bz_narow.py PミンR BzなろうP明朝75-Regular 0.75",
"bz_narow.py PミンR BzなろうP明朝60-Regular 0.6",
"bz_narow.py PミンR BzなろうP明朝50-Regular 0.5",
"bz_narow.py PミンR BzなろうP明朝30-Regular 0.3",
"bz_narow.py PミンB BzなろうP明朝87-Bold 0.875",
"bz_narow.py PミンB BzなろうP明朝75-Bold 0.75",
"bz_narow.py PミンB BzなろうP明朝60-Bold 0.6",
"bz_narow.py PミンB BzなろうP明朝50-Bold 0.5",
"bz_narow.py PミンB BzなろうP明朝30-Bold 0.3",
"bz_narow.py MミンR BzなろうM明朝87-Regular 0.875",
"bz_narow.py MミンR BzなろうM明朝75-Regular 0.75",
"bz_narow.py MミンR BzなろうM明朝60-Regular 0.6",
"bz_narow.py MミンR BzなろうM明朝50-Regular 0.5",
"bz_narow.py MミンR BzなろうM明朝30-Regular 0.3",
"bz_narow.py MミンB BzなろうM明朝87-Bold 0.875",
"bz_narow.py MミンB BzなろうM明朝75-Bold 0.75",
"bz_narow.py MミンB BzなろうM明朝60-Bold 0.6",
"bz_narow.py MミンB BzなろうM明朝50-Bold 0.5",
"bz_narow.py MミンB BzなろうM明朝30-Bold 0.3"
)

# 最大同時実行数
$maxParallel = 10

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
    try {
        $process = Start-Process -FilePath $ffpy -ArgumentList $args -NoNewWindow -PassThru -ErrorAction 'Continue'
        $runningJobs += $process
    } catch {
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