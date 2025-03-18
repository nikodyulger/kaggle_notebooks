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
    latitud: float
    longitud: float
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
            id_estacion=estacion.get("IDEESS", ""),
            direccion=estacion.get("Dirección", ""),
            cod_postal=estacion.get("C.P.", ""),
            latitud=float(estacion.get("Latitud").replace(",", ".")),
            longitud=float(estacion.get("Longitud (WGS84)").replace(",", ".")),
            rotulo=estacion.get("Rótulo", ""),
            horario=estacion.get("Horario", ""),
        )
        gasolineras.append(gasolinera)

    df = pd.DataFrame(gasolineras)
    df.to_csv("data/gasolineras_ab.csv", index=False)

    return gasolineras


def get_precios_gasolineras(data: dict):
    """
    data: dict -> json respuesta API
    {
        "Fecha": "dd/mm/yyyy 0:00:00",
        "ListaEESSPrecio": [
            {
                ...
                "IDEESS": "",
                "Precio Gasoleo A": "1,419",
                "Precio Gasoleo B": "",
                "Precio Gasoleo Premium": "1,459",
                "Precio Gasolina 95 E10": "",
                "Precio Gasolina 95 E5": "1,459",
                "Precio Gasolina 95 E5 Premium": "",
                "Precio Gasolina 98 E10": "",
                "Precio Gasolina 98 E5": "1,659"
                ...
            },
            ...
        ]
    }
    """
    precios = []
    fecha = data.get("Fecha").split(" ")[0]
    precios_estaciones = data.get("ListaEESSPrecio")

    for estacion in precios_estaciones:
        precio_gasoleo_a = estacion.get("Precio Gasoleo A", "").replace(",", ".")
        precio_gasoleo_premium = estacion.get("Precio Gasoleo Premium", "").replace(
            ",", "."
        )
        precio_gasolina_95 = estacion.get("Precio Gasolina 95 E5", "").replace(",", ".")
        precio_gasolina_98 = estacion.get("Precio Gasolina 98 E5", "").replace(",", ".")

        precio = PrecioGasolinera(
            id_estacion=estacion.get("IDEESS"),
            fecha=fecha,
            precio_gasoleo_a=float(precio_gasoleo_a) if precio_gasoleo_a else None,
            precio_gasoleo_premium=(
                float(precio_gasoleo_a) if precio_gasoleo_premium else None
            ),
            precio_gasolina_95=(
                float(precio_gasolina_95) if precio_gasolina_95 else None
            ),
            precio_gasolina_98=(
                float(precio_gasolina_98) if precio_gasolina_98 else None
            ),
        )
        precios.append(precio)

    df = pd.DataFrame(precios)
    df.to_csv("data/precios_gasolineras.csv", index=False)

    return precios


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
    # get_gasolineras_ab(data)  # ejecutar solo una vez
    get_precios_gasolineras(data)  # ejecutar por cada día del año desde 2022 hasta ayer
