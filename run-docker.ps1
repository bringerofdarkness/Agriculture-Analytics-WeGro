$ErrorActionPreference = "Stop"

$ImageName = "wegro-agriculture-api"
$ContainerName = "wegro-agriculture-api"
$HostPort = "8000"
$ContainerPort = "8000"
$HealthUrl = "http://127.0.0.1:$HostPort/health"
$DocsUrl = "http://127.0.0.1:$HostPort/docs"

Write-Host ""
Write-Host "WeGro Agriculture Analytics API - Docker Runner"
Write-Host "================================================"

if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "ERROR: .env file was not found in the project root."
    Write-Host "Create .env using .env.example, then run this script again."
    exit 1
}

try {
    docker --version | Out-Null
} catch {
    Write-Host ""
    Write-Host "ERROR: Docker is not available. Please start Docker Desktop and try again."
    exit 1
}

$RunningContainer = docker ps -aq --filter "name=^/$ContainerName$"

if ($RunningContainer) {
    Write-Host ""
    Write-Host "Removing existing container: $ContainerName"
    docker rm -f $ContainerName | Out-Null
}

Write-Host ""
Write-Host "Building Docker image: $ImageName"
docker build -t $ImageName .

Write-Host ""
Write-Host "Starting container on port $HostPort..."
docker run -d `
    --name $ContainerName `
    --env-file .env `
    -p "${HostPort}:${ContainerPort}" `
    $ImageName | Out-Null

Write-Host ""
Write-Host "Waiting for health check..."

$Healthy = $false

for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 2

    try {
        $Response = Invoke-RestMethod $HealthUrl -TimeoutSec 3
        if ($Response.status -eq "healthy") {
            $Healthy = $true
            break
        }
    } catch {
        Write-Host "Waiting... attempt $i"
    }
}

if (-not $Healthy) {
    Write-Host ""
    Write-Host "ERROR: Container started, but health check did not pass."
    Write-Host "Container logs:"
    docker logs $ContainerName
    exit 1
}

Write-Host ""
Write-Host "Container is healthy."
Write-Host ""
Write-Host "Swagger UI: $DocsUrl"
Write-Host "Health URL: $HealthUrl"
Write-Host ""
Write-Host "Useful commands:"
Write-Host "  docker logs $ContainerName"
Write-Host "  docker stop $ContainerName"
Write-Host "  docker rm $ContainerName"
Write-Host ""
