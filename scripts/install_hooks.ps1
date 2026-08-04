$ErrorActionPreference = "Stop"
git config core.hooksPath .githooks
Write-Host "Git hooks enabled. index.json will be synchronized before every commit."
