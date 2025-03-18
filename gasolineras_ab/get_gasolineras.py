import json
import time
import pandas as pd
import requests as req
from dataclasses import dataclass, asdict
from rich.pretty import pprint


# Doc de la API https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/help
@dataclass
class Gasolinera:
    id_estacion: str
    direccion: str
    cod_postal: str
    latitud: str
    longitud: str
    rotulo: str
    horario: str
    municipio: str = "Albacete"


@dataclass
class PrecioGasolinera:
    id_estacion: str
    fecha: str
    precio_gasoleo_a: float = None
    precio_gasoleo_premium: float = None
    precio_gasolina_95: float = None
    precio_gasolina_98: float = None


def get_comunidades_autonomas():
    URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/Listados/ComunidadesAutonomas/"

    res = req.get(URL)
    data = res.json()

    with open("data/comunidades.json", "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_provincias():
    URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/Listados/Provincias/"

    res = req.get(URL)
    data = res.json()

    with open("data/provincias.json", "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_municipios():
    URL = "https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/Listados/Municipios/"

    res = req.get(URL)
    data = res.json()

    with open("data/municipios.json", "w") as f:
        json.dump(data, f, indent=4)

    return data


def get_precios_fecha_municipio(fecha: str, id_municipio: str):
    """
    fecha -> formato dd-mm-aaaa
    id_municipio -> uno valido de la lista de municipios
    """

    URL = f"https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/EstacionesTerrestresHist/FiltroMunicipio/{fecha}/{id_municipio}"

    res = req.get(URL)
    data = res.json()
    return data


def get_gasolineras_ab(data: dict):
    """
    data: dict -> json respuesta API
    {
        "Fecha": "dd/mm/yyyy 0:00:00",
        "ListaEESSPrecio": [
            {
                "C.P.": "",
                "Dirección": "",
                "Horario": "",
                "Latitud": "",
                "Localidad": "",
                "Longitud (WGS84)": ""
                ...
            },
            ...
        ]
    }
    """
    gasolineras = []
    precios_estaciones = data["ListaEESSPrecio"]
    for estacion in precios_estaciones:
        gasolinera = Gasolinera(
            id_estacion=estacion["IDEESS"],
            direccion=estacion["Dirección"],
            cod_postal=estacion["C.P."],
            latitud=estacion["Latitud"],
            longitud=estacion["Longitud (WGS84)"],
            rotulo=estacion["Rótulo"],
            horario=estacion["Horario"],
        )
        gasolineras.append(gasolinera)

    df = pd.DataFrame(gasolineras)
    df.to_csv("data/gasolineras_ab.csv", index=False)

    return gasolineras


"""
    {
        "IDMunicipio": "54",
        "IDProvincia": "02",
        "IDCCAA": "07",
        "Municipio": "Albacete",
        "Provincia": "ALBACETE",
        "CCAA": "Castilla la Mancha"
    },
"""

if __name__ == "__main__":
    # get_comunidades_autonomas()
    # get_provincias()
    # get_municipios()
    data = get_precios_fecha_municipio("15-02-2025", "54")
    get_gasolineras_ab(data)  # ejecutar solo una vez
