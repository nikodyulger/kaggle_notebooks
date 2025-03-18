import json
import requests as req


# Doc de la API https://sedeaplicaciones.minetur.gob.es/ServiciosRESTCarburantes/PreciosCarburantes/help


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
    get_municipios()
