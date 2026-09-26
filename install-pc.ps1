# One-line SamiLang installer for Windows (no admin, no git required).
# Paste this in PowerShell:
#   irm https://raw.githubusercontent.com/Samiullah-khan-devx/Samilang/main/install-pc.ps1 | iex
$ErrorActionPreference = "Stop"
$repo = "Samiullah-khan-devx/Samilang"
$bin = "$env:LOCALAPPDATA\Programs\samilang"
$dst = Join-Path $bin "repo"

# 1. Python (winget fallback)
try { & python --version 2>$null | Out-Null; $hasPy = $true } catch { $hasPy = $false }
if (-not $hasPy) {
  Write-Host "Installing Python via winget..."
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
  $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}
& python --version

# 2. numpy
python -m pip install --quiet numpy

# 3. SamiLang source
New-Item -ItemType Directory -Force $bin | Out-Null
if ((Get-Command git -ErrorAction SilentlyContinue) -and (Test-Path (Join-Path $dst ".git"))) {
  git -C $dst pull --ff-only 2>$null | Out-Null
} elseif (Get-Command git -ErrorAction SilentlyContinue) {
  if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
  git clone --depth 1 "https://github.com/$repo.git" $dst
} else {
  $zip = Join-Path $env:TEMP "samilang.zip"
  Invoke-WebRequest -Uri "https://codeload.github.com/$repo/zip/refs/heads/main" -OutFile $zip
  if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
  Expand-Archive $zip -DestinationPath (Join-Path $bin "tmp") -Force
  Move-Item (Join-Path $bin "tmp\Samilang-main") $dst
  Remove-Item -Recurse -Force (Join-Path $bin "tmp"), $zip
}

# 4. `samilang` command shim + PATH
Set-Content (Join-Path $bin "samilang.cmd") "@echo off`r`npython `"$dst\lang\__main__.py`" %*`r`n" -Encoding Ascii
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$bin*") {
  [Environment]::SetEnvironmentVariable("Path", "$userPath;$bin", "User")
}
if ($env:Path -notlike "*$bin*") { $env:Path += ";$bin" }
Add-Type -Namespace Win32 -Name EnvNotify -MemberDefinition @"
[System.Runtime.InteropServices.DllImport("user32.dll", SetLastError=true, CharSet=System.Runtime.InteropServices.CharSet.Auto)]
public static extern int SendMessageTimeout(int hWnd, int Msg, int wParam, string lParam, int flags, int timeout, out int result);
"@ | Out-Null
$result = 0
[Win32.EnvNotify]::SendMessageTimeout(0xFFFF, 0x1A, 0, "Environment", 2, 5000, [ref]$result) | Out-Null

# 5. Prove it
& (Join-Path $bin "samilang.cmd") --version
Write-Host "Done. Open a NEW terminal, then: samilang examples\\hello.sm"
Write-Host "(examples live in $dst\\examples)"
