import requests
from patient import create_patient_resource

BASE_URL = "https://hapi.fhir.org/baseR4"


#Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource, resource_type):
    url = f"{BASE_URL}/{resource_type}"
    headers = {"Content-Type": "application/fhir+json"}
    resource_json = resource.json()

    response = requests.post(url, headers=headers, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")

        # Devolver el ID del recurso creado
        return response.json()['id']
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None


#Buscar el recurso por ID
def get_resource_from_hapi_fhir(resource_id, resource_type):
    url = f"{BASE_URL}/{resource_type}/{resource_id}"
    response = requests.get(url, headers={"Accept": "application/fhir+json"})

    if response.status_code == 200:
        resource = response.json()
        print(resource)
        return resource
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())
        return None


#Buscar pacientes por número de documento (Actividad 3.b)
# Usa el parámetro de búsqueda "identifier" con el formato system|value, así se busca el DNI dentro del sistema de RENAPER y no cualquier identifier.
def search_patient_by_dni(dni, system="http://www.renaper.gob.ar/dni"):
    url = f"{BASE_URL}/Patient"
    params = {"identifier": f"{system}|{dni}"}
    response = requests.get(url, params=params, headers={"Accept": "application/fhir+json"})

    if response.status_code != 200:
        print(f"Error en la búsqueda: {response.status_code}")
        print(response.json())
        return []

    #La respuesta es un Bundle de tipo "searchset" con los resultados en "entry"
    bundle = response.json()
    patients = [entry["resource"] for entry in bundle.get("entry", [])]
    print(f"Pacientes encontrados con DNI {dni}: {len(patients)}")
    for p in patients:
        name = p.get("name", [{}])[0]
        full_name = " ".join(name.get("given", []) + [name.get("family", "")]).strip()
        print(f"  - Patient/{p['id']}: {full_name}")
    return patients