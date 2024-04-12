import csv
import os
import time

campos = ["Fecha (DD-MM-YYYY)", "Hora (24)", "Riego", "Volumen (L)", "Humedad (0-1)", "Sistema Utilizado"]

filepath = 'database/'
filename = filepath + 'datos_riego_inteligente.csv'

def actualizar_base_de_datos(filename, data):
    '''
    data: una lista de campos para anadir a la base de datos
    e.g. ["11-4-2024", 1, 22.2, 0.576, "Inteligente"]
    '''
    if not os.path.exists(filename):
        # Crear un CSV file con los 
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(campos)
        
    with open(filename, 'a', newline="") as fd:
        csvwriter = csv.writer(fd)
        csvwriter.writerow(data)

