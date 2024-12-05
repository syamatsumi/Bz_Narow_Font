# FontForgeを実行
$fontforge = "C:\Program Files (x86)\FontForgeBuilds\bin\ffpython.exe"

# 実行するコマンドのリスト
$commands = @(
    "bz_narow.py MゴシR Bzなろうゴシック90-Regular 0.9",
    "bz_narow.py MゴシR Bzなろうゴシック75-Regular 0.75",
    "bz_narow.py MゴシR Bzなろうゴシック50-Regular 0.5",
    "bz_narow.py MゴシB Bzなろうゴシック90-Bold 0.9",
    "bz_narow.py MゴシB Bzなろうゴシック75-Bold 0.75",
    "bz_narow.py MゴシB Bzなろうゴシック50-Bold 0.5",
    "bz_narow.py PゴシR BzなろうPゴシック90-Regular 0.9",
    "bz_narow.py PゴシR BzなろうPゴシック75-Regular 0.75",
    "bz_narow.py PゴシR BzなろうPゴシック50-Regular 0.5",
    "bz_narow.py PゴシB BzなろうPゴシック90-Bold 0.9",
    "bz_narow.py PゴシB BzなろうPゴシック75-Bold 0.75",
    "bz_narow.py PゴシB BzなろうPゴシック50-Bold 0.5",
    "bz_narow.py MミンR Bzなろう明朝90-Regular 0.9",
    "bz_narow.py MミンR Bzなろう明朝75-Regular 0.75",
    "bz_narow.py MミンR Bzなろう明朝50-Regular 0.5",
    "bz_narow.py MミンB Bzなろう明朝90-Bold 0.9",
    "bz_narow.py MミンB Bzなろう明朝75-Bold 0.75",
    "bz_narow.py MミンB Bzなろう明朝50-Bold 0.5",
    "bz_narow.py PミンR BzなろうP明朝90-Regular 0.9",
    "bz_narow.py PミンR BzなろうP明朝75-Regular 0.75",
    "bz_narow.py PミンR BzなろうP明朝50-Regular 0.5",
    "bz_narow.py PミンB BzなろうP明朝90-Bold 0.9",
    "bz_narow.py PミンB BzなろうP明朝75-Bold 0.75",
    "bz_narow.py PミンB BzなろうP明朝50-Bold 0.5"
)

# 最大同時実行数
$maxParallel = 8

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

    # コマンドを実行
    Write-Host "Executing: $fontforge $args"
    try {
        $process = Start-Process -FilePath $fontforge -ArgumentList $args -NoNewWindow -PassThru -ErrorAction 'Continue'
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
