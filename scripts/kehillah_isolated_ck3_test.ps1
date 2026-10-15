# Launch CK3 against this checkout with a separate user directory, mod registration,
# saves, settings, run scripts, and logs. Visible mode is for an available test display.
param(
    [switch]$Visible,
    [string]$ProfileRoot = (Join-Path $env:USERPROFILE '.codex\ck3-test\festival-observance')
)

$ErrorActionPreference = 'Stop'
$gameExe = 'E:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\binaries\ck3.exe'
$repoRoot = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$profileRoot = [System.IO.Path]::GetFullPath($ProfileRoot)

if (-not (Test-Path -LiteralPath $gameExe)) {
    throw "CK3 executable not found: $gameExe"
}

$existing = Get-CimInstance Win32_Process -Filter "name='ck3.exe'" |
    Where-Object { $_.CommandLine -like "*userdir=$($profileRoot.Replace('\', '/'))*" }
if ($existing) {
    throw "CK3 already uses the isolated profile (PID $($existing.ProcessId -join ', '))."
}

$modDir = Join-Path $profileRoot 'mod'
New-Item -ItemType Directory -Path $modDir -Force | Out-Null
$modPath = Join-Path $modDir 'jewishcommunities_codex.mod'
$registration = @"
version="0.1"
tags={
    "1.20 'Crozier'"
}
name="Jewish Communities (Codex Test)"
supported_version="1.20.*"
path="$($repoRoot.Replace('\', '/'))"
"@
Set-Content -LiteralPath $modPath -Value $registration -Encoding utf8
Set-Content -LiteralPath (Join-Path $profileRoot 'dlc_load.json') -Value '{"enabled_mods":["mod/jewishcommunities_codex.mod"],"disabled_dlcs":[]}' -Encoding utf8

$launchArgs = @('-debug_mode', '-develop', '-gdpr-compliant', "-userdir=$($profileRoot.Replace('\', '/'))")
if ($Visible) {
    $process = Start-Process -FilePath $gameExe -ArgumentList $launchArgs -WindowStyle Normal -PassThru
} else {
    $process = Start-Process -FilePath $gameExe -ArgumentList $launchArgs -WindowStyle Hidden -PassThru
}
[pscustomobject]@{
    ProcessId = $process.Id
    Checkout = $repoRoot
    Profile = $profileRoot
    DebugLog = (Join-Path $profileRoot 'logs\debug.log')
    Visible = [bool]$Visible
}

