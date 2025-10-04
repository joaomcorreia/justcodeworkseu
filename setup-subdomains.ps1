# JustCodeWorks.EU Subdomain Setup Script
# Run this in PowerShell as Administrator

Write-Host "🚀 Setting up JustCodeWorks.EU subdomains for local development..." -ForegroundColor Cyan

$hostsPath = "$env:windir\System32\drivers\etc\hosts"

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Backup hosts file
$backupPath = "$hostsPath.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
Copy-Item $hostsPath $backupPath
Write-Host "📋 Backed up hosts file to: $backupPath" -ForegroundColor Green

# Customer subdomains to add
$subdomains = @(
    "vakwerkpro.justcodeworks.eu",
    "bouwbedrijf-amsterdam.justcodeworks.eu", 
    "techsolutions.justcodeworks.eu",
    "webstudio-delft.justcodeworks.eu",
    "schilder-partners.justcodeworks.eu"
)

Write-Host "`n🔧 Adding subdomain entries..." -ForegroundColor Cyan

$hostsContent = Get-Content $hostsPath
$added = 0

foreach ($subdomain in $subdomains) {
    $entry = "127.0.0.1    $subdomain"
    
    if ($hostsContent -notcontains $entry) {
        Add-Content $hostsPath $entry
        Write-Host "✅ Added: $subdomain" -ForegroundColor Green
        $added++
    } else {
        Write-Host "⚠️  Already exists: $subdomain" -ForegroundColor Yellow
    }
}

if ($added -gt 0) {
    Write-Host "`n🔄 Flushing DNS cache..." -ForegroundColor Cyan
    ipconfig /flushdns | Out-Null
}

Write-Host "`n🎉 Subdomain setup complete!" -ForegroundColor Green
Write-Host "`n📝 Test these URLs (after starting Django server):" -ForegroundColor Cyan
Write-Host "   • http://vakwerkpro.justcodeworks.eu:8001/" -ForegroundColor White
Write-Host "   • http://techsolutions.justcodeworks.eu:8001/" -ForegroundColor White
Write-Host "   • http://bouwbedrijf-amsterdam.justcodeworks.eu:8001/" -ForegroundColor White
Write-Host "`n🔧 Admin panels:" -ForegroundColor Cyan
Write-Host "   • http://vakwerkpro.justcodeworks.eu:8001/admin/" -ForegroundColor White
Write-Host "   • http://techsolutions.justcodeworks.eu:8001/admin/" -ForegroundColor White

Write-Host "`n💡 Main site unchanged: http://127.0.0.1:8001/" -ForegroundColor Cyan
Write-Host "`nPress any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")