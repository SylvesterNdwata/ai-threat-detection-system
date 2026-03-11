param(
    [string]$Goal = "exec:java"
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

function Get-MavenCommand {
    $mvnFromPath = Get-Command mvn.cmd -ErrorAction SilentlyContinue
    if ($mvnFromPath) {
        return $mvnFromPath.Source
    }

    $candidates = @(
        "C:\maven\apache-maven-3.9.13\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.12\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.11\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.10\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.9\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.8\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.7\bin\mvn.cmd",
        "C:\maven\apache-maven-3.9.6\bin\mvn.cmd",
        "C:\Program Files\Apache\maven\bin\mvn.cmd",
        "C:\Program Files\Apache\Maven\bin\mvn.cmd",
        "C:\apache-maven\bin\mvn.cmd"
    )

    foreach ($path in $candidates) {
        if (Test-Path $path) {
            return $path
        }
    }

    throw "Maven not found. Install Maven or add mvn.cmd to PATH."
}

$mvn = Get-MavenCommand
Write-Host "Using Maven: $mvn"

& $mvn $Goal
