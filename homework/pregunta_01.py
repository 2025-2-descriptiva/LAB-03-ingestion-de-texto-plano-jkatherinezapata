"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import re
def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    import pandas as pd

    ruta = "files/input/clusters_report.txt"

    patron_inicio = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")
    registros = []

    with open(ruta, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    actual = None 

    for linea in lineas:
        linea = linea.rstrip("\n")

    
        m = patron_inicio.match(linea)
        if m:
      
            if actual is not None:

                termos = actual["principales_palabras_clave"]
                termos = termos.strip()
                if termos.endswith("."):
                    termos = termos[:-1]
        
                partes = [p.strip() for p in termos.split(",") if p.strip() != ""]
                actual["principales_palabras_clave"] = ", ".join(partes)
                registros.append(actual)

            cluster = int(m.group(1))
            cantidad = int(m.group(2))
            porcentaje_txt = m.group(3).replace(",", ".")
            porcentaje = round(float(porcentaje_txt), 1)
            resto = m.group(4).strip()

            actual = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": porcentaje,
                "principales_palabras_clave": resto,
            }
            continue


        if actual is not None:
            cont = linea.strip()
            if cont:  
                actual["principales_palabras_clave"] += " " + cont


    if actual is not None:
        termos = actual["principales_palabras_clave"].strip()
        if termos.endswith("."):
            termos = termos[:-1]
        partes = [p.strip() for p in termos.split(",") if p.strip() != ""]
        actual["principales_palabras_clave"] = ", ".join(partes)
        registros.append(actual)


    df = pd.DataFrame(registros, columns=[
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ])

    return df