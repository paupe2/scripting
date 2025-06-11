# Obtener perfiles WiFi guardados
$profiles = netsh wlan show profiles | Select-String "Perfil de todos los usuarios" | ForEach-Object {
    ($_ -split ":")[1].Trim()
}

if (-not $profiles) {
    Write-Host "No se encontraron redes Wi-Fi guardadas."
    exit
}

# Mostrar menú
Write-Host "Redes Wi-Fi guardadas:"
for ($i=0; $i -lt $profiles.Count; $i++) {
    Write-Host "$($i+1). $($profiles[$i])"
}

do {
    $choice = Read-Host "Selecciona el número de la red para ver la contraseña"
} while (-not ([int]::TryParse($choice, [ref]$null) -and $choice -ge 1 -and $choice -le $profiles.Count))

$ssid = $profiles[$choice - 1]

Write-Host "`nContraseña para '$ssid':"
$profile_info = netsh wlan show profile name="$ssid" key=clear

$key_line = $profile_info | Select-String "Contenido de la clave"

if ($key_line) {
    $password = ($key_line -split ":")[1].Trim()
    Write-Host $password
} else {
    Write-Host "No se encontró contraseña o está vacía."
}

