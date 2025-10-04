# Subdomain Setup for JustCodeWorks.EU Local Development

## Automatic Setup (Run as Administrator)

**Option 1: PowerShell Script (Recommended)**

```powershell
# Run PowerShell as Administrator, then run this:
$hostsPath = "$env:windir\System32\drivers\etc\hosts"
$entries = @(
    "127.0.0.1    vakwerkpro.justcodeworks.eu",
    "127.0.0.1    bouwbedrijf-amsterdam.justcodeworks.eu", 
    "127.0.0.1    techsolutions.justcodeworks.eu",
    "127.0.0.1    webstudio-delft.justcodeworks.eu",
    "127.0.0.1    schilder-partners.justcodeworks.eu"
)

foreach ($entry in $entries) {
    if ((Get-Content $hostsPath) -notcontains $entry) {
        Add-Content $hostsPath $entry
        Write-Host "Added: $entry" -ForegroundColor Green
    } else {
        Write-Host "Already exists: $entry" -ForegroundColor Yellow
    }
}
Write-Host "`n✅ Subdomain setup complete!" -ForegroundColor Green
```

## Manual Setup

**Option 2: Edit hosts file manually**

1. **Open Notepad as Administrator**
2. **Open file**: `C:\Windows\System32\drivers\etc\hosts`
3. **Add these lines at the end**:

```
127.0.0.1    vakwerkpro.justcodeworks.eu
127.0.0.1    bouwbedrijf-amsterdam.justcodeworks.eu
127.0.0.1    techsolutions.justcodeworks.eu
127.0.0.1    webstudio-delft.justcodeworks.eu
127.0.0.1    schilder-partners.justcodeworks.eu
```

4. **Save and close**

## Test the Setup

After adding the hosts entries, test these URLs:

### Customer Websites:
- **VakWerk Pro**: http://vakwerkpro.justcodeworks.eu:8001/
- **TechSolutions**: http://techsolutions.justcodeworks.eu:8001/
- **Bouwbedrijf**: http://bouwbedrijf-amsterdam.justcodeworks.eu:8001/

### Customer Admin Panels:
- **VakWerk Admin**: http://vakwerkpro.justcodeworks.eu:8001/admin/
- **TechSolutions Admin**: http://techsolutions.justcodeworks.eu:8001/admin/

### Main JustCodeWorks Site:
- **Main Site**: http://127.0.0.1:8001/ (unchanged)

## Troubleshooting

If subdomains don't work:
1. **Flush DNS**: `ipconfig /flushdns` in cmd
2. **Restart browser** 
3. **Check hosts file** syntax (no extra spaces)
4. **Run as Administrator** when editing hosts

## Production Setup

In production, these would be real DNS entries:
- vakwerkpro.justcodeworks.eu → Your server IP
- techsolutions.justcodeworks.eu → Your server IP
- etc.

The Django application will handle routing automatically!