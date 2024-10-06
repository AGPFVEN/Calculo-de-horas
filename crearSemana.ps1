# Directorio donde están los archivos .txt de origen
$sourceDir = "./"

# Ruta completa del archivo de destino
$destinationFile = "./esta_semana.txt"

# Obtener todos los archivos .txt en el directorio de origen
$txtFiles = Get-ChildItem -Path $sourceDir -Filter "*-*-*.txt"

# Si el archivo de destino ya existe, se elimina para evitar duplicados
if (Test-Path $destinationFile) {
    Remove-Item $destinationFile
}

# Iterar sobre cada archivo .txt y agregar su contenido al archivo de destino
foreach ($file in $txtFiles) {
    # Leer el contenido del archivo actual
    Write-Host "Se subio $file"
    $content = Get-Content -Path $file.FullName

    # Agregar el contenido al archivo de destino
    Add-Content -Path $destinationFile -Value $content
}

Write-Host "Archivos combinados exitosamente en $destinationFile"

python .\timem.py $destinationFile