# 构建 Windows 文件夹版发行包
$ErrorActionPreference = "Stop"
$projectRoot = $PSScriptRoot
Set-Location $projectRoot

$pyInstaller = Join-Path $projectRoot ".venv\Scripts\pyinstaller.exe"
if (-not (Test-Path -LiteralPath $pyInstaller)) {
    throw "找不到 PyInstaller，请先安装 requirements-build.txt。"
}

Write-Host "开始构建 DocumentToMarkdown..."
& $pyInstaller --noconfirm DocumentToMarkdown.spec
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller 构建失败，退出代码：$LASTEXITCODE"
}

$packageDirectory = Join-Path $projectRoot "dist\DocumentToMarkdown"
if (-not (Test-Path -LiteralPath $packageDirectory)) {
    throw "没有找到构建目录：$packageDirectory"
}

$usageSource = Join-Path $projectRoot "package-assets\usage.txt"
$usageTarget = Join-Path $packageDirectory "使用说明.txt"
Copy-Item -LiteralPath $usageSource -Destination $usageTarget -Force

$releaseDirectory = Join-Path $projectRoot "release"
New-Item -ItemType Directory -Path $releaseDirectory -Force | Out-Null
$zipPath = Join-Path $releaseDirectory "DocumentToMarkdown-Windows-x64.zip"

Write-Host "正在生成压缩包..."
Compress-Archive -Path $packageDirectory -DestinationPath $zipPath -Force

$hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash
$hashPath = Join-Path $releaseDirectory "SHA256.txt"
"$hash  DocumentToMarkdown-Windows-x64.zip" | Set-Content -LiteralPath $hashPath -Encoding ascii

Write-Host "构建完成：$zipPath"
Write-Host "SHA256：$hash"