from datetime import datetime
import sys
import os

# Función para calcular la diferencia entre dos horas
def calcular_diferencia(hora1: datetime, hora2:datetime):
    formato = "%H:%M"
    h1 = datetime.strptime(hora1, formato)
    h2 = datetime.strptime(hora2, formato)
    diferencia = h2 - h1
    return diferencia

# Asegurarse que el archivo tenga una linea extra
with open(sys.argv[1], 'rb+') as archivo:
    
    #Add newline if there is none
    archivo.seek(-1, os.SEEK_END)
    if archivo.read(1) != b"\n":
        archivo.write(b"\n")

# Leer el archivo y procesar las líneas
resultados = {}
descripciones = {}
hora_previa = ""
resultado = datetime.strptime("00:00", "%H:%M")
with open(sys.argv[1], 'r+', encoding="utf8") as archivo:
    for linea in archivo:
        descripcion_aux = ""
        partes = linea.strip().split()
        horas = []
        en_parentesis = 0
        for i in partes:
            if en_parentesis == 1:
                if i[-1] == ')':
                    en_parentesis = 0
                    descripcion_aux += " " + i[:-1]
                else:
                    descripcion_aux += " " + i
            elif i[0].isdigit() == True:
                horas.append(i)
            elif i[0] == '(':
                if i[-1] == ')':
                    descripcion_aux = i[1:-1]
                else:
                    descripcion_aux = i[1:]
                    en_parentesis = 1
            else:
                nombre = i
        
        if len(horas) == 1:
            horas.insert(0, hora_previa)

        hora_previa = horas[1]

        diferencia = calcular_diferencia(horas[0], horas[1])
        resultado += diferencia
        if nombre in resultados:
            resultados[nombre] += diferencia
        else:
            resultados[nombre] = diferencia

        if (descripcion_aux == ""):
            descripcion_aux = "non-specified"

        if nombre not in descripciones:
            descripciones[nombre] = {}

        if descripcion_aux in descripciones[nombre]:
            descripciones[nombre][descripcion_aux] += diferencia.seconds
        else:
            descripciones[nombre][descripcion_aux] = diferencia.seconds
    
# Mostrar los resultados
for nombre, diferencia in resultados.items():
    sys.stdout.buffer.write(f"{nombre}: {diferencia}\n".encode("utf8"))
    if nombre in descripciones:
        for i in descripciones[nombre]:
                sys.stdout.buffer.write((f"   + {i}: {int(descripciones[nombre][i] / 3600)}h {int((descripciones[nombre][i] % 3600) / 60)}min\n".encode("utf8")))

print(f"Total de horas: {str(resultado.hour + ((resultado.day - 1) * 24))}h {str(resultado.minute)}mins")

# Guardar los resultados en una lista
lista_resultados = [(nombre, diferencia) for nombre, diferencia in resultados.items()]