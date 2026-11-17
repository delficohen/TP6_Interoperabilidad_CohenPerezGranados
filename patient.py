from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.identifier import Identifier
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding

# Sistema de identificación del DNI argentino (RENAPER), el mismo que usan
# los perfiles FHIR de Argentina para el documento único.
DNI_SYSTEM = "http://www.renaper.gob.ar/dni"


# Crear el recurso FHIR de paciente con parámetros opcionales
def create_patient_resource(family_name=None, given_name=None, birth_date=None,
                            gender=None, phone=None, dni=None):
    patient = Patient()

    #Agregamos el número de documento como identifier (Actividad 3.a)
    if dni:
        identifier = Identifier()
        identifier.use = "official"
        identifier.type = CodeableConcept(
            coding=[Coding(
                system="http://terminology.hl7.org/CodeSystem/v2-0203",
                code="NI",
                display="National unique individual identifier",
            )],
            text="DNI",
        )
        identifier.system = DNI_SYSTEM
        identifier.value = str(dni)
        patient.identifier = [identifier]

    # Agregar el nombre del paciente si está disponible
    if family_name or given_name:
        name = HumanName()
        if family_name:
            name.family = family_name
        if given_name:
            name.given = [given_name]
        patient.name = [name]

    # Agregar la fecha de nacimiento si está disponible
    if birth_date:
        patient.birthDate = birth_date

    # Agregar el género si está disponible
    if gender:
        patient.gender = gender

    # Agregar información de contacto si está disponible
    if phone:
        contact = ContactPoint()
        contact.system = "phone"
        contact.value = phone
        contact.use = "mobile"
        patient.telecom = [contact]

    return patient