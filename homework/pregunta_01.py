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

    import pandas as pd

    ruta = "files/input/clusters_report.txt"


    pat_inicio = re.compile(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)$")

    with open(ruta, "r", encoding="utf-8") as f:

        lineas = f.readlines()[4:]

    registros = []
    actual = None

    def cerrar_actual():
        """Normaliza el campo 'principales_palabras_clave' y guarda el registro."""
        if actual is None:
            return
        texto = actual["principales_palabras_clave"].strip()


        texto = re.sub(r"\s+", " ", texto)


        if texto.endswith("."):
            texto = texto[:-1]


        partes = [p.strip() for p in texto.split(",") if p.strip()]
        actual["principales_palabras_clave"] = ", ".join(partes)

        registros.append(actual)

    for linea in lineas:
        linea = linea.rstrip("\n")


        if not linea.strip() or set(linea.strip()) == {"-"}:
            continue

        m = pat_inicio.match(linea)
        if m:

            if actual is not None:
                cerrar_actual()

            cluster = int(m.group(1))
            cantidad = int(m.group(2))
            porcentaje = float(m.group(3).replace(",", "."))
            resto = m.group(4).strip()

            actual = {
                "cluster": cluster,
                "cantidad_de_palabras_clave": cantidad,
                "porcentaje_de_palabras_clave": round(porcentaje, 1),
                "principales_palabras_clave": resto,
            }
        else:

            if actual is not None:

                actual["principales_palabras_clave"] += " " + linea.strip()

    if actual is not None:
        cerrar_actual()

    df = pd.DataFrame(
        registros,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    return df