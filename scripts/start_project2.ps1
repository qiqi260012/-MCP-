param(
    [string]$Python = ".\.venv\Scripts\python.exe"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$project = Join-Path $root "mcp_lecture_project\project2_Agent_SDK+MCP_materials"
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
    @{ Name = "stock_predict_mcp"; Script = "stock_predict_mcp_server.py" },
    @{ Name = "article_check_mcp"; Script = "article_check_mcp_server.py" },
    @{ Name = "finance_consult_mcp"; Script = "finance_consult_mcp_server.py" },
    @{ Name = "finance_api"; Script = "chat_api.py" },
    @{ Name = "gradio_ui"; Script = "gradio_demo.py" }
)

foreach ($svc in $services) {
    Write-Host "Starting $($svc.Name) ..."
    Start-Process -FilePath $pythonPath -ArgumentList $svc.Script -WorkingDirectory $project -WindowStyle Hidden
    Start-Sleep -Seconds 2
}

Write-Host "Project 2 services started."
Write-Host "API:    http://127.0.0.1:9998/finance_MultiAgent_MultiMCP"
Write-Host "Gradio: http://127.0.0.1:9996"

