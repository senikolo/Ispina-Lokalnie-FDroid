$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$apkName = 'Ispina-Lokalnie-Live-1.83.20.apk'
$apkUrl = 'https://github.com/senikolo/Ispina-Lokalnie-/releases/download/v1.83.20/Ispina-Lokalnie-Live-1.83.20.apk'
$expectedSha256 = 'c9c0a0107310c3229b421a87832de1f1fc738b07db7ab1dc41eea2ead417e664'
$repoDir = Join-Path $root 'repo'
$apkPath = Join-Path $repoDir $apkName
$temporaryPath = "$apkPath.tmp"

New-Item -ItemType Directory -Force -Path $repoDir | Out-Null
Invoke-WebRequest -Uri $apkUrl -OutFile $temporaryPath
$actualSha256 = (Get-FileHash -Path $temporaryPath -Algorithm SHA256).Hash.ToLowerInvariant()

if ($actualSha256 -ne $expectedSha256) {
    Remove-Item -Force -ErrorAction SilentlyContinue $temporaryPath
    throw "Suma SHA-256 nie zgadza się z wydaniem 1.83.20. Otrzymano: $actualSha256"
}

Move-Item -Force $temporaryPath $apkPath
Write-Host "Pobrano i sprawdzono APK: $apkPath"
