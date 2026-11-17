from patient import create_patient_resource
from encounter import create_encounter_resource
from base import (send_resource_to_hapi_fhir, get_resource_from_hapi_fhir,
                  search_patient_by_dni)

if __name__ == "__main__":
    #Actividad 3.a: crear un Patient con DNI y leerlo 
    family_name = "Gonzalez"
    given_name = "Martín"
    birth_date = "1970-05-10"
    gender = "male"
    phone = None
    dni = "21349725"   

    patient = create_patient_resource(family_name, given_name, birth_date, gender, phone, dni)
    patient_id = send_resource_to_hapi_fhir(patient, 'Patient')

    if patient_id:
        print(f"\nPatient creado con id {patient_id}. Leyendo el recurso:")
        get_resource_from_hapi_fhir(patient_id, 'Patient')

    #Actividad 3.b: buscar el paciente por documento
    print("\nBuscando paciente por DNI:")
    search_patient_by_dni(dni)

    #Actividad 3.c: crear un Encounter para ese paciente
    if patient_id:
        encounter = create_encounter_resource(
            patient_id,
            status="finished",
            class_code="AMB",
            start="2026-10-10T10:00:00-03:00",
            end="2026-10-10T10:30:00-03:00",
            reason="Control clínico anual",
            practitioner_name="Dra. Marta Gómez",
            organization_name="Hospital Rivadavia",
        )
        encounter_id = send_resource_to_hapi_fhir(encounter, 'Encounter')

        if encounter_id:
            print(f"\nEncounter creado con id {encounter_id}. Leyendo el recurso:")
            get_resource_from_hapi_fhir(encounter_id, 'Encounter')