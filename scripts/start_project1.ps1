param(
    [string]$Python = ".\.venv\Scripts\python.exe"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root "mcp_lecture_project\project1_stock_counselor"
$pythonPath = Join-Path $root $Python
$envFile = Join-Path $project ".env"

if (-not (Test-Path $pythonPath)) {
    throw "Virtual environment Python not found: $pythonPath. Run: python -m venv .venv"
}

if (-not (Test-Path $envFile)) {
    throw "Missing .env file: $envFile. Copy .env.example to .env and fill your API keys."
}

$services = @(
    @{ Name = "turn_human_mcp"; Script = "turn_human_server.py" },
    @{ Name = "stock_mcp"; Script = "stock_sever.py" },
    @{ Name = "policy_reply_mcp"; Script = "policy_reply_server.py" }
)

foreach ($svc in $services) {
    Write-Host "Starting $($svc.Name) ..."
    Start-Process -FilePath $pythonPath -ArgumentList $svc.Script -WorkingDirectory $project -WindowStyle Hidden
    Start-Sleep -Seconds 2
}

Write-Host "Project 1 MCP services started."
Write-Host "Interactive client:"
Write-Host "  cd $project"
Write-Host "  $pythonPath multi_sse_mcp_client.py"
