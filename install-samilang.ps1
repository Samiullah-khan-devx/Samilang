# Installs the `samilang` command on this PC (current user, no admin needed).
# Run: powershell -ExecutionPolicy Bypass -File install-samilang.ps1
$ErrorActionPreference = "Stop"
$root = Split-Path $MyInvocation.MyCommand.Path
$bin = "$env:LOCALAPPDATA\Programs\samilang"
New-Item -ItemType Directory -Force $bin | Out-Null
$runner = Join-Path $root "lang\__main__.py"
Set-Content -Path (Join-Path $bin "samilang.cmd") -Value "@echo off`r`npython `"$runner`" %*`r`n" -Encoding Ascii

$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$bin*") {
  [Environment]::SetEnvironmentVariable("Path", "$userPath;$bin", "User")
  Write-Host "Added to user PATH: $bin"
} else {
  Write-Host "Already on user PATH: $bin"
}
if ($env:Path -notlike "*$bin*") { $env:Path += ";$bin" }

# Notify running programs of the env change so new terminals pick it up.
Add-Type -Namespace Win32 -Name EnvNotify -MemberDefinition @"
[System.Runtime.InteropServices.DllImport("user32.dll", SetLastError=true, CharSet=System.Runtime.InteropServices.CharSet.Auto)]
public static extern int SendMessageTimeout(int hWnd, int Msg, int wParam, string lParam, int flags, int timeout, out int result);
"@ | Out-Null
$result = 0
[Win32.EnvNotify]::SendMessageTimeout(0xFFFF, 0x1A, 0, "Environment", 2, 5000, [ref]$result) | Out-Null

Write-Host "samilang installed. Open a NEW terminal and run: samilang --version"
