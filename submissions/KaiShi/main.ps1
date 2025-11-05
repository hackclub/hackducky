$ErrorActionPreference = "Continue"
Set-ExecutionPolicy Bypass -Scope Process -Force
Write-Host "Starting script..."

Write-Host "Installing Chocolatey..."
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

Write-Host "Installing Apps..."
choco install shutup10 discord firefox steam nodejs powertoys k-litecodecpackfull qbittorrent python git putty obs-studio.install -y   
winget install -e --id Mojang.MinecraftLauncher

# various config
OOSU10.exe OOSU10.cfg /nosrp
netsh interface ipv4 set dnsservers name="Wi-Fi" static 1.1.1.1 index=1 # what happened to index 0 lmao
netsh interface ipv4 set dnsservers name="Wi-Fi" static 1.0.0.1 index=2
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "HideFileExt" -Value 0
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced" -Name "Hidden" -Value 1
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

Write-Host "Disabling mouse acceleration..."
Set-ItemProperty -Path "HKCU:\Control Panel\Mouse\" -Name "MouseSpeed" -Value 0
Set-ItemProperty -Path "HKCU:\Control Panel\Mouse\" -Name "MouseThreshold1" -Value 0
Set-ItemProperty -Path "HKCU:\Control Panel\Mouse\" -Name "MouseThreshold2" -Value 0

Write-Host "Enabling Dark Mode..."
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "AppsUseLightTheme" -Value 0
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "SystemUsesLightTheme" -Value 0
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced\TaskbarDeveloperSettings" -Name "TaskbarEndTask" -Value 1 # i opened up a whole ahh procmon for ts but it's worth it
reg add "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock" /t REG_DWORD /f /v "AllowDevelopmentWithoutDevLicense" /d "1"
sudo config --enable enable

Write-Host "Editing PATH..."
$path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine')
$newPath = "$path;C:\Users\Public\wpilib\2025\vscode\bin"
[System.Environment]::SetEnvironmentVariable('Path', $newPath, 'Machine')

Write-Host "Downloading WPILib..."
$response = Invoke-RestMethod "https://api.github.com/repos/wpilibsuite/allwpilib/releases/latest"
$body = $response.body
if ($body -match "(https[^\s`"']*WPILib_Windows[^\s`"'\)]*)") {
    $url = $matches[1]
    Write-Output $url

    Invoke-WebRequest -Uri $url -OutFile "wpilib.iso"
}

$mnt = Mount-DiskImage -ImagePath "./wpilib.iso" -PassThru  
$isodrive = ($mnt | Get-Volume).DriveLetter + ":" # this feels hacky but i bet everything feels hacky in powershell
mkdir wpilib # call me linux
Copy-Item -Path "$isodrive\*" -Destination "./wpilib" -Recurse -Force
./wpilib/wpilib.exe
# configure your own installation bozo
Write-Host "Installing Linux..."
wsl --install # ts so Wait... This isn't what I typed! now
Start-Process "https://imgur.com/a/name-4k-wallpaper-galore-ShAOh" # 50-50 they want to use ts wallpapers so leave it there
Start-Process "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
Start-Process "https://github.com/Sreekar617/setup-ducky"
