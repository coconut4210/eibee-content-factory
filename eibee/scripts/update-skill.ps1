param(
    [string]$Ref = "main"
)

$ErrorActionPreference = "Stop"
$skillRoot = Split-Path -Parent $PSScriptRoot
$repository = "coconut4210/eibee-content-factory"
$rawBase = "https://raw.githubusercontent.com/$repository/$Ref/eibee"
$temporarySkill = Join-Path $env:TEMP ("eibee-skill-" + [guid]::NewGuid().ToString() + ".md")
$temporaryVersion = Join-Path $env:TEMP ("eibee-version-" + [guid]::NewGuid().ToString() + ".txt")

try {
    Invoke-WebRequest -Uri "$rawBase/SKILL.md" -OutFile $temporarySkill
    Invoke-WebRequest -Uri "$rawBase/VERSION" -OutFile $temporaryVersion

    if (-not (Select-String -Path $temporarySkill -Pattern '^name: eibee$' -Quiet)) {
        throw "Downloaded file is not the eibee Skill. Nothing was changed."
    }

    $newVersion = (Get-Content -Raw $temporaryVersion).Trim()
    if ($newVersion -notmatch '^\d+\.\d+\.\d+$') {
        throw "Downloaded version is invalid. Nothing was changed."
    }

    $currentSkill = Join-Path $skillRoot "SKILL.md"
    $currentVersion = Join-Path $skillRoot "VERSION"
    Copy-Item -LiteralPath $currentSkill -Destination "$currentSkill.bak" -Force
    Copy-Item -LiteralPath $temporarySkill -Destination $currentSkill -Force
    Set-Content -LiteralPath $currentVersion -Value $newVersion -NoNewline
    Write-Output "eibee updated to $newVersion from $Ref. Backup: $currentSkill.bak"
}
finally {
    Remove-Item -LiteralPath $temporarySkill -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $temporaryVersion -Force -ErrorAction SilentlyContinue
}
