# PowerShell script to label and lock all closed issues in a repo
# Usage: pwsh ./scripts/label-and-lock-closed-issues.ps1

param(
  [string]$owner = 'dougis-org',
  [string]$repo = 'laravel-recipes-2025',
  [string]$labelName = 'archived',
  [string]$labelColor = 'FF8800',
  [string]$labelDesc = "Archived closed issues (added by automation)"
)

function Ensure-GhAvailable {
  if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Error "GitHub CLI 'gh' not found on PATH. Install from https://cli.github.com/ and run 'gh auth login'."
    exit 2
  }
}

function Ensure-Label {
  param($labelName, $labelColor, $labelDesc)
  $exists = gh label view $labelName --repo $owner/$repo -q 'name' 2>$null
  if (-not $?) {
    Write-Host "Creating label '$labelName'..."
    gh label create $labelName --color $labelColor --description $labelDesc --repo $owner/$repo
  } else {
    Write-Host "Label '$labelName' already exists."
  }
}

function Get-ClosedIssues {
  # returns array of issue numbers
  $json = gh issue list --repo $owner/$repo --state closed --limit 1000 --json number,title,url
  if (-not $?) { throw "Failed to list issues via gh." }
  return ($json | ConvertFrom-Json)
}

function Process-Issues {
  param($issues, $labelName)
  foreach ($issue in $issues) {
    $n = $issue.number
    Write-Host "Processing issue #$n - $($issue.title)"
    gh issue edit $n --add-label $labelName --repo $owner/$repo
    gh issue lock $n --repo $owner/$repo
  }
}

# Main
Ensure-GhAvailable
Ensure-Label -labelName $labelName -labelColor $labelColor -labelDesc $labelDesc
$closed = Get-ClosedIssues
if ($closed.Count -eq 0) { Write-Host "No closed issues found."; exit 0 }
Process-Issues -issues $closed -labelName $labelName
Write-Host "Done: labeled and locked $($closed.Count) closed issues."