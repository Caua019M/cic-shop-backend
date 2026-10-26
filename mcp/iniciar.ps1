$ErrorActionPreference = 'Stop'

$python = Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
if (-not (Test-Path -LiteralPath $python)) {
    $command = Get-Command python -ErrorAction SilentlyContinue
    if (-not $command) {
        throw 'Python 3.11+ não encontrado. Instale o Python e execute este script novamente.'
    }
    $python = $command.Source
}

$venv = Join-Path $PSScriptRoot '.venv'
$venvPython = Join-Path $venv 'Scripts/python.exe'
if (-not (Test-Path -LiteralPath $venvPython)) {
    & $python -m venv $venv
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível criar o ambiente Python.' }
}

& $venvPython -c 'import mcp.server.mcpserver' 2>$null
if ($LASTEXITCODE -ne 0) {
    & $venvPython -m pip install 'mcp>=2.0.0,<3'
    if ($LASTEXITCODE -ne 0) { throw 'Não foi possível instalar o SDK MCP.' }
}

Write-Host 'CIC SHOP MCP: http://127.0.0.1:8141/mcp'
& $venvPython (Join-Path $PSScriptRoot 'app.py')
