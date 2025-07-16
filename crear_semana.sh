#!/bin/bash

# Directorio donde están los archivos .txt de origen
sourceDir="./"

# Ruta completa del archivo de destino
destinationFile="./esta_semana.txt"

# Obtener todos los archivos .txt con formato de fecha (dd-mm-yyyy.txt)
txtFiles=$(find "$sourceDir" -maxdepth 1 -type f -name "*-*-*.txt")

# Si el archivo de destino ya existe, se elimina para evitar duplicados
if [ -f "$destinationFile" ]; then
    rm "$destinationFile"
fi

# Iterar sobre cada archivo .txt y agregar su contenido al archivo de destino
for file in $txtFiles; do
    echo "Se subió $file"
    cat "$file" >> "$destinationFile"
done

echo "Archivos combinados exitosamente en $destinationFile"

python3 ./timem.py "$destinationFile"
