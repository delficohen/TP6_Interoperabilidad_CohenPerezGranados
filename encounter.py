from fhir.resources.encounter import Encounter, EncounterParticipant
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.reference import Reference
from fhir.resources.period import Period


#Crear el recurso FHIR Encounter (Actividad 3.c)
#Un Encounter es una interacción entre un paciente y uno o más prestadores de salud (consulta, internación, guardia, etc.). Se vincula al paciente mediante una referencia "Patient/id".
def create_encounter_resource(patient_id, status="finished", class_code="AMB",
                              start=None, end=None, reason=None,
                              practitioner_name=None, organization_name=None):
    encounter = Encounter.construct()

    #status (obligatorio) es el estado del encuentro: planned | arrived | triaged | in-progress | onleave | finished | cancelled | etc
    encounter.status = status

    #class (obligatorio) es la clasificación del encuentro, según HL7 v3 ActCode: AMB = ambulatorio, IMP = internación, EMER = emergencia, HH = domiciliario
    class_display = {
        "AMB": "ambulatory",
        "IMP": "inpatient encounter",
        "EMER": "emergency",
        "HH": "home health",
    }
    encounter.class_fhir = Coding(
        system="http://terminology.hl7.org/CodeSystem/v3-ActCode",
        code=class_code,
        display=class_display.get(class_code),
    )

    #type: tipo específico de encuentro (codificado con SNOMED CT)
    encounter.type = [CodeableConcept(
        coding=[Coding(
            system="http://snomed.info/sct",
            code="11429006",
            display="Consultation",
        )],
        text="Consulta",
    )]

    #subject: el paciente al que corresponde el encuentro (relación entre recursos)
    encounter.subject = Reference(reference=f"Patient/{patient_id}")

    # participant: profesionales que intervienen en el encuentro
    if practitioner_name:
        encounter.participant = [EncounterParticipant(
            type=[CodeableConcept(
                coding=[Coding(
                    system="http://terminology.hl7.org/CodeSystem/v3-ParticipationType",
                    code="PPRF",
                    display="primary performer",
                )]
            )],
            individual=Reference(display=practitioner_name),
        )]

    #period: inicio y fin del encuentro
    if start or end:
        encounter.period = Period(start=start, end=end)

    #reasonCode: motivo de la consulta
    if reason:
        encounter.reasonCode = [CodeableConcept(text=reason)]

    #serviceProvider: organización responsable del encuentro
    if organization_name:
        encounter.serviceProvider = Reference(display=organization_name)

    #Validar el recurso completo contra el modelo FHIR
    return Encounter.parse_obj(encounter.dict())