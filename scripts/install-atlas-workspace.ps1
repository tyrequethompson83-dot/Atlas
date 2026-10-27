[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'Medium')]
param(
    # Supply this when OpenClaw's active agent uses a non-default workspace.
    [string]$WorkspacePath
)

$ErrorActionPreference = 'Stop'

$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$sourceRoot = [System.IO.Path]::GetFullPath((Join-Path $repoRoot 'atlas-workspace'))

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "ATLAS workspace pack was not found at: $sourceRoot"
}

if ([string]::IsNullOrWhiteSpace($WorkspacePath)) {
    if (-not [string]::IsNullOrWhiteSpace($env:OPENCLAW_WORKSPACE_DIR)) {
        $WorkspacePath = $env:OPENCLAW_WORKSPACE_DIR
    }
    else {
        $WorkspacePath = Join-Path $HOME '.openclaw\workspace'
    }
}

$WorkspacePath = [System.IO.Path]::GetFullPath($WorkspacePath)
$repoPrefix = $repoRoot.TrimEnd([char[]]@('\', '/')) + [System.IO.Path]::DirectorySeparatorChar
$workspaceNormalized = $WorkspacePath.TrimEnd([char[]]@('\', '/'))

if (
    $workspaceNormalized.Equals($repoRoot.TrimEnd([char[]]@('\', '/')), [System.StringComparison]::OrdinalIgnoreCase) -or
    $workspaceNormalized.StartsWith($repoPrefix, [System.StringComparison]::OrdinalIgnoreCase)
) {
    throw "Refusing to install the workspace into the source checkout: $WorkspacePath"
}

$sourceFiles = @(Get-ChildItem -LiteralPath $sourceRoot -File -Recurse)
if ($sourceFiles.Count -eq 0) {
    throw "The ATLAS workspace pack is empty: $sourceRoot"
}

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$backupRoot = Join-Path (Join-Path $HOME '.openclaw\backups') "atlas-workspace-$stamp"
$installed = 0
$backedUp = 0
$unchanged = 0

Write-Host "ATLAS workspace source: $sourceRoot"
Write-Host "Target OpenClaw workspace: $WorkspacePath"
Write-Host "Existing files will be backed up before being replaced."

foreach ($sourceFile in $sourceFiles) {
    $relativePath = [System.IO.Path]::GetRelativePath($sourceRoot, $sourceFile.FullName)
    $destination = Join-Path $WorkspacePath $relativePath

    if (Test-Path -LiteralPath $destination) {
        $existing = Get-Item -LiteralPath $destination -Force

        if ($existing.PSIsContainer) {
            throw "A directory exists where a workspace file should go; refusing to replace it: $destination"
        }
        if (-not [string]::IsNullOrWhiteSpace([string]$existing.LinkType)) {
            throw "Refusing to replace a linked file; inspect it manually first: $destination"
        }

        $sourceHash = (Get-FileHash -LiteralPath $sourceFile.FullName -Algorithm SHA256).Hash
        $destinationHash = (Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash
        if ($sourceHash -eq $destinationHash) {
            Write-Host "Already current: $relativePath"
            $unchanged++
            continue
        }
    }

    if ($PSCmdlet.ShouldProcess($destination, 'Install ATLAS workspace file')) {
        $destinationDirectory = Split-Path -Parent $destination
        New-Item -ItemType Directory -Path $destinationDirectory -Force | Out-Null

        if (Test-Path -LiteralPath $destination -PathType Leaf) {
            $backupPath = Join-Path $backupRoot $relativePath
            New-Item -ItemType Directory -Path (Split-Path -Parent $backupPath) -Force | Out-Null
            Copy-Item -LiteralPath $destination -Destination $backupPath
            $backedUp++
            Write-Host "Backed up: $relativePath"
        }

        Copy-Item -LiteralPath $sourceFile.FullName -Destination $destination -Force
        $installed++
        Write-Host "Installed: $relativePath"
    }
}

Write-Host ''
Write-Host "ATLAS workspace install complete. Installed: $installed; backed up: $backedUp; already current: $unchanged."

if ($backedUp -gt 0) {
    Write-Host "Backup location: $backupRoot"
}
Write-Host 'This installs workspace instructions and one example skill only; it does not configure model credentials or enable external integrations.'
