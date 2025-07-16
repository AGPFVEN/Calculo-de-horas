#!/bin/bash

# Obtener el primer parámetro
p1="$1"

# Componer fecha
if [ -n "$p1" ]; then
    mydate="$p1"
else
    mydate="$(date +%d-%m-%Y).txt"
fi

# Verificar si el archivo existe y es un archivo regular
if [ -f "$mydate" ]; then
    python3 ./timem.py "$mydate"
else
    touch "$mydate"
fi
